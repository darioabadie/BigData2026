# Databricks notebook source
"""Utilidades del laboratorio de MLflow (clase 5).

El caso sigue siendo el de fraude en e-commerce. En las clases anteriores
`is_fraud` era una alerta generada por una regla fija. Ahora el área de riesgo
entrega qué transacciones terminaron en **contracargo confirmado**
(`chargeback`), y queremos un modelo que lo anticipe.

La etiqueta se genera de forma determinista a partir de las transacciones,
clientes y productos Silver: depende de varias señales combinadas y tiene ruido,
como un dato real. Nadie la conoce de antemano salvo este helper.
"""

import warnings

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from mlflow.models import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix, f1_score,
                             precision_recall_curve, precision_score, recall_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ML_LABEL_SEED = 20261015
CLASS_TAG = "5"
RANDOM_STATE = 42

# Split temporal: se entrena con el pasado y se evalúa con el día siguiente.
# El último día se reserva como "transacciones nuevas" para el scoring batch.
SPLITS = ("train", "test", "nuevas")

NUMERIC_FEATURES = ["amount", "hour", "is_night", "day_of_week", "account_age_days",
                    "price", "amount_to_price", "device_customers", "rule_alert"]
CATEGORICAL_FEATURES = ["payment_channel", "segment", "country", "category"]

FEATURE_SETS = {
    "solo_regla": ["rule_alert"],
    "basicas": ["amount", "payment_channel"],
    "cliente": ["amount", "payment_channel", "hour", "account_age_days", "segment", "country"],
    "completas": ["amount", "payment_channel", "hour", "is_night", "day_of_week", "account_age_days",
                  "segment", "country", "category", "price", "amount_to_price", "device_customers"],
}

MODEL_TYPES = ("logistic_regression", "random_forest", "gradient_boosting")

# Valores ofrecidos en los widgets del notebook 02 (y recorridos por el barrido).
WIDGET_CHOICES = {
    "modelo": list(MODEL_TYPES),
    "features": list(FEATURE_SETS),
    "class_weight": ["ninguno", "balanced"],
    "umbral": ["0.5", "0.4", "0.3", "0.2"],
    "C": ["0.01", "0.1", "1", "10"],
    "n_estimators": ["50", "100", "200"],
    "max_depth": ["3", "5", "8", "sin_limite"],
    "learning_rate": ["0.03", "0.1", "0.3"],
}

# Qué hiperparámetros usa cada modelo (el resto se ignora y no se registra).
MODEL_PARAMS = {
    "logistic_regression": ["C"],
    "random_forest": ["n_estimators", "max_depth"],
    "gradient_boosting": ["learning_rate", "max_depth"],
}


# ---------------------------------------------------------------------------
# Datos
# ---------------------------------------------------------------------------

def ml_features_query(config):
    """SELECT que arma la tabla de features con la etiqueta y el split."""
    tx = qualified_table(config, "silver_transactions")
    customers = qualified_table(config, "silver_customers")
    products = qualified_table(config, "silver_products")
    return f"""
WITH base AS (
  SELECT t.transaction_id, t.customer_id, t.event_ts,
         CAST(t.amount AS DOUBLE) AS amount, t.payment_channel, t.device_id,
         t.is_fraud AS rule_alert,
         c.segment, c.country, c.created_date, p.category, CAST(p.price AS DOUBLE) AS price
  FROM {tx} t
  JOIN {customers} c ON t.customer_id = c.customer_id
  JOIN {products} p ON t.product_id = p.product_id
  WHERE t.source_batch_id = 'initial'
), devices AS (
  SELECT device_id, COUNT(DISTINCT customer_id) AS device_customers FROM base GROUP BY device_id
), features AS (
  SELECT b.transaction_id, b.customer_id, b.event_ts,
         b.amount, b.payment_channel,
         CAST(hour(b.event_ts) AS INT) AS hour,
         CAST(hour(b.event_ts) < 6 AS INT) AS is_night,
         CAST(dayofweek(b.event_ts) AS INT) AS day_of_week,
         CAST(datediff(to_date(b.event_ts), b.created_date) AS INT) AS account_age_days,
         b.segment, b.country, b.category, b.price,
         ROUND(b.amount / b.price, 4) AS amount_to_price,
         CAST(d.device_customers AS INT) AS device_customers,
         CAST(b.rule_alert AS INT) AS rule_alert
  FROM base b JOIN devices d ON b.device_id = d.device_id
), scored AS (
  SELECT *,
         -6.0
         + 3.0 / (1 + exp(-(amount - 1400) / 100))
         + 1.2 * CAST(payment_channel = 'transfer' AS INT)
         + 1.8 * is_night * CAST(payment_channel <> 'card' AS INT)
         + 0.4 * is_night
         + 1.5 * CAST(account_age_days < 180 AS INT)
         + 0.7 * CAST(segment = 'new' AS INT)
         + 1.5 * CAST(category = 'electronics' AND amount > 800 AS INT)
         + 0.8 * CAST(device_customers >= 4 AS INT)
         + 0.4 * CAST(country IN ('MX', 'BR') AS INT) AS _logit,
         pmod(xxhash64(transaction_id, {ML_LABEL_SEED}), 1000000) / 1000000.0 AS _noise
  FROM features
)
SELECT transaction_id, customer_id, event_ts,
       CASE WHEN to_date(event_ts) <= DATE'2026-03-05' THEN 'train'
            WHEN to_date(event_ts) = DATE'2026-03-06' THEN 'test'
            ELSE 'nuevas' END AS split,
       amount, payment_channel, hour, is_night, day_of_week, account_age_days,
       segment, country, category, price, amount_to_price, device_customers, rule_alert,
       CAST(_noise < 1 / (1 + exp(-_logit)) AS INT) AS chargeback
FROM scored
"""


def build_ml_features(spark, config):
    """Crea (o reemplaza) la tabla ml_features y la devuelve."""
    table = qualified_table(config, "ml_features")
    (spark.sql(ml_features_query(config)).write.mode("overwrite")
     .option("overwriteSchema", "true").saveAsTable(table))
    return spark.table(table)


def load_split(spark, config, split):
    """Trae un split a pandas con los tipos que espera scikit-learn."""
    if split not in SPLITS:
        raise ValueError(f"Split inválido: {split}")
    pdf = spark.table(qualified_table(config, "ml_features")).where(f"split = '{split}'").toPandas()
    return clean_types(pdf)


def clean_types(pdf):
    pdf = pdf.copy()
    for column in NUMERIC_FEATURES:
        if column in pdf:
            pdf[column] = pdf[column].astype("float64")
    for column in CATEGORICAL_FEATURES:
        if column in pdf:
            pdf[column] = pdf[column].astype(str)
    if "chargeback" in pdf:
        pdf["chargeback"] = pdf["chargeback"].astype(int)
    return pdf.sort_values("transaction_id").reset_index(drop=True)


# ---------------------------------------------------------------------------
# MLflow: experimento y modelos
# ---------------------------------------------------------------------------

def experiment_path(spark, config):
    user = spark.sql("SELECT current_user()").first()[0]
    return f"/Users/{user}/bigdata_{config.student_id}_clase05"


def setup_experiment(spark, config, path=None):
    """Crea o reutiliza el experimento del alumno y lo deja activo.

    Desactiva el autologging automático: los runs de la práctica registran
    siempre las mismas métricas con nombres propios, para poder compararlos.
    """
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", message=".*solver options.*")
    path = path or experiment_path(spark, config)
    experiment = mlflow.set_experiment(path)
    mlflow.autolog(disable=True)
    return experiment


def table_version(spark, table):
    """Versión Delta de una tabla (para registrar qué datos se usaron)."""
    try:
        return str(spark.sql(f"DESCRIBE HISTORY {table}").agg({"version": "max"}).first()[0])
    except Exception:  # noqa: BLE001 - fuera de Delta no hay historial
        return "n/a"


def base_tags(config, notebook):
    return {"clase": CLASS_TAG, "student_id": config.student_id, "scale": config.scale, "notebook": notebook}


def parse_param(name, value):
    """Convierte el texto de un widget en el valor que espera scikit-learn."""
    if name == "max_depth":
        return None if value in (None, "sin_limite", "None") else int(value)
    if name == "n_estimators":
        return int(value)
    if name in ("C", "learning_rate", "umbral"):
        return float(value)
    if name == "class_weight":
        return None if value in (None, "ninguno", "None") else value
    return value


def split_columns(features):
    numeric = [f for f in features if f in NUMERIC_FEATURES]
    categorical = [f for f in features if f in CATEGORICAL_FEATURES]
    return numeric, categorical


def build_pipeline(model_type, features, class_weight=None, C=1.0, n_estimators=100,
                   max_depth=None, learning_rate=0.1):
    """Preprocesamiento + modelo en un único Pipeline (se registra entero)."""
    numeric, categorical = split_columns(features)
    transformers = []
    if numeric:
        transformers.append(("num", StandardScaler(), numeric))
    if categorical:
        transformers.append(("cat", OneHotEncoder(handle_unknown="ignore"), categorical))
    if model_type == "logistic_regression":
        model = LogisticRegression(C=C, class_weight=class_weight, max_iter=1000)
    elif model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, class_weight=class_weight,
                                       min_samples_leaf=1, n_jobs=-1, random_state=RANDOM_STATE)
    elif model_type == "gradient_boosting":
        model = HistGradientBoostingClassifier(learning_rate=learning_rate, max_depth=max_depth, max_iter=150,
                                               class_weight=class_weight, random_state=RANDOM_STATE)
    else:
        raise ValueError(f"Modelo desconocido: {model_type}")
    return Pipeline([("preprocesamiento", ColumnTransformer(transformers)), ("modelo", model)])


def evaluate(scores, y, threshold, prefix):
    predicted = (scores >= threshold).astype(int)
    return {
        f"{prefix}_pr_auc": float(average_precision_score(y, scores)),
        f"{prefix}_roc_auc": float(roc_auc_score(y, scores)),
        f"{prefix}_accuracy": float(accuracy_score(y, predicted)),
        f"{prefix}_precision": float(precision_score(y, predicted, zero_division=0)),
        f"{prefix}_recall": float(recall_score(y, predicted, zero_division=0)),
        f"{prefix}_f1": float(f1_score(y, predicted, zero_division=0)),
        f"{prefix}_alertas": int(predicted.sum()),
    }


def confusion_figure(y, scores, threshold, title):
    matrix = confusion_matrix(y, (scores >= threshold).astype(int), labels=[0, 1])
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    ax.imshow(matrix, cmap="Blues")
    for (i, j), value in np.ndenumerate(matrix):
        ax.text(j, i, f"{value:,}", ha="center", va="center",
                color="white" if value > matrix.max() / 2 else "black", fontsize=11)
    ax.set_xticks([0, 1], ["no alerta", "alerta"])
    ax.set_yticks([0, 1], ["sin contracargo", "contracargo"])
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Realidad")
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    return fig


def pr_curve_figure(y, scores, threshold, title):
    precision, recall, thresholds = precision_recall_curve(y, scores)
    fig, ax = plt.subplots(figsize=(4.8, 3.6))
    ax.plot(recall, precision, color="#2563eb")
    ax.axhline(y.mean(), color="#94a3b8", ls="--", label=f"azar = {y.mean():.3f}")
    predicted = scores >= threshold
    if predicted.any():
        ax.scatter([recall_score(y, predicted)], [precision_score(y, predicted, zero_division=0)],
                   color="#dc2626", zorder=3, label=f"umbral {threshold}")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title(title, fontsize=10)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return fig


def importance_frame(pipeline, X, y, features, max_rows=2000):
    """Importancia por permutación sobre las columnas originales (igual para todos los modelos)."""
    sample = X.sample(min(max_rows, len(X)), random_state=RANDOM_STATE)
    result = permutation_importance(pipeline, sample[features], y.loc[sample.index], scoring="average_precision",
                                    n_repeats=3, random_state=RANDOM_STATE, n_jobs=1)
    return (pd.DataFrame({"feature": features, "importancia": result.importances_mean})
            .sort_values("importancia", ascending=False).reset_index(drop=True))


def importance_figure(importance, title):
    fig, ax = plt.subplots(figsize=(5.2, max(2.2, 0.35 * len(importance) + 1)))
    ordered = importance.iloc[::-1]
    ax.barh(ordered["feature"], ordered["importancia"], color="#16a34a")
    ax.set_xlabel("Caída del PR-AUC al desordenar la columna")
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    return fig


def log_sklearn_model(pipeline, X_example):
    """Registra el Pipeline con firma y ejemplo de entrada (compatible con MLflow 2 y 3)."""
    signature = infer_signature(X_example, pipeline.predict(X_example))
    # cloudpickle: el formato que entienden tanto MLflow 2 como MLflow 3 (que por defecto usa skops)
    kwargs = dict(sk_model=pipeline, signature=signature, input_example=X_example.head(5),
                  serialization_format="cloudpickle")
    if int(mlflow.__version__.split(".")[0]) >= 3:
        info = mlflow.sklearn.log_model(name="model", **kwargs)
    else:
        info = mlflow.sklearn.log_model(artifact_path="model", **kwargs)
    return info.model_uri


def train_and_log(train, test, config, notebook, model_type, feature_set, class_weight=None, threshold=0.5,
                  run_name=None, nested=False, extra_tags=None, data_version="n/a", **hyperparams):
    """Entrena un Pipeline, lo evalúa y registra todo en un run de MLflow.

    Devuelve un diccionario con el run_id, la URI del modelo y las métricas.
    """
    features = FEATURE_SETS[feature_set]
    used = {name: hyperparams[name] for name in MODEL_PARAMS[model_type] if name in hyperparams}
    pipeline = build_pipeline(model_type, features, class_weight=class_weight, **used)
    X_train, y_train = train[features], train["chargeback"]
    X_test, y_test = test[features], test["chargeback"]

    tags = {**base_tags(config, notebook), "tipo": "modelo", **(extra_tags or {})}
    with mlflow.start_run(run_name=run_name, nested=nested, tags=tags) as run:
        mlflow.log_params({"model_type": model_type, "feature_set": feature_set,
                           "class_weight": class_weight or "ninguno", "threshold": threshold,
                           "n_features": len(features), "train_rows": len(train), "test_rows": len(test),
                           "data_table": "ml_features", "data_version": data_version,
                           **{k: ("sin_limite" if v is None else v) for k, v in used.items()}})
        pipeline.fit(X_train, y_train)
        train_scores = pipeline.predict_proba(X_train)[:, 1]
        test_scores = pipeline.predict_proba(X_test)[:, 1]
        metrics = {**evaluate(test_scores, y_test, threshold, "test"),
                   "train_pr_auc": float(average_precision_score(y_train, train_scores))}
        mlflow.log_metrics(metrics)

        label = f"{model_type} · {feature_set} · umbral {threshold}"
        figures = {
            "matriz_confusion.png": confusion_figure(y_test, test_scores, threshold, label),
            "curva_precision_recall.png": pr_curve_figure(y_test, test_scores, threshold, label),
        }
        importance = importance_frame(pipeline, X_test, y_test, features)
        figures["importancia_features.png"] = importance_figure(importance, label)
        for name, fig in figures.items():
            mlflow.log_figure(fig, name)
        mlflow.log_text(importance.to_csv(index=False), "importancia_features.csv")

        model_uri = log_sklearn_model(pipeline, X_test)
        mlflow.set_tag("model_uri", model_uri)
        run_id = run.info.run_id

    for fig in figures.values():
        plt.close(fig)   # se muestran a pedido con display(fig): evita gráficos repetidos en los barridos
    return {"run_id": run_id, "model_uri": model_uri, "metrics": metrics, "importance": importance,
            "pipeline": pipeline, "test_scores": test_scores, "figures": figures}


# ---------------------------------------------------------------------------
# Consultar runs
# ---------------------------------------------------------------------------

RUN_COLUMNS = {
    "tags.mlflow.runName": "run",
    "params.model_type": "modelo",
    "params.feature_set": "features",
    "params.class_weight": "class_weight",
    "params.threshold": "umbral",
    "params.C": "C",
    "params.n_estimators": "n_estimators",
    "params.max_depth": "max_depth",
    "params.learning_rate": "learning_rate",
    "metrics.train_pr_auc": "train_pr_auc",
    "metrics.test_pr_auc": "pr_auc",
    "metrics.test_roc_auc": "roc_auc",
    "metrics.test_accuracy": "accuracy",
    "metrics.test_precision": "precision",
    "metrics.test_recall": "recall",
    "metrics.test_f1": "f1",
    "tags.notebook": "notebook",
    "tags.model_uri": "model_uri",
    "run_id": "run_id",
}


def my_runs(config, experiment_id):
    """Runs de modelos del alumno en su experimento, del mejor al peor PR-AUC."""
    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        filter_string=f"tags.clase = '{CLASS_TAG}' AND tags.student_id = '{config.student_id}' AND tags.tipo = 'modelo'",
        order_by=["metrics.test_pr_auc DESC"],
    )
    if runs.empty:
        return pd.DataFrame(columns=list(RUN_COLUMNS.values()))
    for column in RUN_COLUMNS:
        if column not in runs:
            runs[column] = None
    table = runs[list(RUN_COLUMNS)].rename(columns=RUN_COLUMNS)
    for column in ["train_pr_auc", "pr_auc", "roc_auc", "accuracy", "precision", "recall", "f1"]:
        table[column] = table[column].astype(float).round(3)
    return table.reset_index(drop=True)


def hyperparams_text(row):
    """Resume en un texto los hiperparámetros que usó cada modelo."""
    names = MODEL_PARAMS.get(row.get("modelo"), [])
    values = [(name, row.get(name)) for name in names]
    return ", ".join(f"{name}={value}" for name, value in values if value is not None and not pd.isna(value) and value != "")


def markdown_table(frame, columns, max_rows=15):
    """Tabla Markdown para copiar en el README (sin dependencias externas)."""
    rows = frame[columns].head(max_rows).fillna("")
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join(["---"] * len(columns)) + "|"]
    for _, row in rows.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in columns) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Registro en Unity Catalog
# ---------------------------------------------------------------------------

def registered_model_name(config, catalog):
    return f"{catalog}.{config.schema}.fraud_model"


def register_champion(model_uri, name, alias="champion", registry_uri="databricks-uc"):
    """Registra el modelo en Unity Catalog y le asigna un alias.

    Si el registro falla (por ejemplo, por una limitación del entorno), devuelve
    la URI del run para que la práctica pueda continuar.
    """
    try:
        mlflow.set_registry_uri(registry_uri)
        version = mlflow.register_model(model_uri, name)
        MlflowClient().set_registered_model_alias(name, alias, version.version)
        return {"registered": True, "uri": f"models:/{name}@{alias}", "version": str(version.version), "error": None}
    except Exception as error:  # noqa: BLE001 - se informa y se sigue con la URI del run
        return {"registered": False, "uri": model_uri, "version": None, "error": f"{type(error).__name__}: {str(error)[:400]}"}
