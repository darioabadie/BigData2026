# Clase práctica 5 — MLOps con MLflow: experimentar, comparar, registrar y monitorear

## Propósito

Entrenar modelos sobre la misma plataforma de e-commerce y gestionarlos con **MLflow**, como se hace en un equipo de datos: cada entrenamiento queda registrado, los resultados se comparan con la métrica adecuada, el mejor modelo se registra con un nombre y un alias, se usa para puntuar transacciones nuevas y se controla cuando llegan los resultados reales.

**El problema.** En las clases anteriores `is_fraud` era una alerta generada por una regla fija. Ahora el área de riesgo nos pasa qué transacciones terminaron en **contracargo confirmado** (`chargeback`) y queremos un modelo que lo anticipe con los datos disponibles al momento de la compra.

A diferencia de las clases 3 y 4, **en esta práctica experimentás vos**: en el notebook 02 elegís el modelo, las variables y los hiperparámetros con **widgets**, sin escribir código, y cada ejecución queda como un run en tu experimento. Los notebooks 00, 01, 03 y 04 son demostrativos: se ejecutan en orden sin modificar nada.

## Objetivos

- Explicar qué guarda MLflow en un run (parámetros, métricas, artefactos, modelo, firma) y qué agrega autolog.
- Reconocer qué hace reproducible un experimento: datos, código, semilla y entorno.
- Comparar modelos con una métrica adecuada a clases desbalanceadas (PR-AUC) y entender por qué la accuracy engaña.
- Detectar sobreajuste comparando métricas de entrenamiento y de test.
- Separar el modelo (que ordena el riesgo) del umbral (que decide cuántas alertas se generan).
- Registrar un modelo con versión y alias, usarlo en inferencia batch con trazabilidad y monitorearlo.

## Requisitos previos

- Clase 2 ejecutada: se usan `silver_customers`, `silver_products` y `silver_transactions`.
- Mismo `student_id` y misma escala que en las clases anteriores (se recomienda `small`).
- Compute serverless. No hay que instalar librerías: MLflow, scikit-learn, pandas y matplotlib vienen con la plataforma.
- Para importación manual, conservar `clase-05/` y `common/` como carpetas hermanas.

## Secuencia

Ejecutá los notebooks en orden. El 00 crea la tabla `ml_features` y tu experimento; los demás la usan.

| Notebook | Tema de la teoría | Qué se ve | Minutos |
|---|---|---|---:|
| `00_preflight.ipynb` | Datos para ML, split temporal | Verifica las tablas de la clase 2, arma `ml_features` y crea el experimento | 10 |
| `01_primer_run.ipynb` | Tracking: experimento, run, parámetros, métricas, artefactos | Un run a mano y otro con autolog; reproducibilidad; cargar el modelo y su firma | 20 |
| `02_mis_experimentos.ipynb` | Experimentación, hiperparámetros, sobreajuste | **Tus runs** con widgets y un barrido de un hiperparámetro | 30 |
| `03_comparar_y_elegir.ipynb` | Comparación y selección de modelos | Tus runs como tabla; mejor por PR-AUC vs. por accuracy; gráficos; tabla para la entrega | 15 |
| `04_registro_y_uso.ipynb` | Model Registry, alias, inferencia batch, monitoreo, drift | Registro en Unity Catalog con alias `champion`; scoring de transacciones nuevas; monitoreo y drift simulado | 20 |

## Los datos

`ml_features` tiene una fila por transacción de la carga inicial, unida con su cliente y su producto, con variables derivadas (hora, antigüedad de la cuenta, clientes por dispositivo, etc.) y la etiqueta `chargeback`. Los contracargos son alrededor del 10 % de las compras: las clases están **desbalanceadas**.

La partición es **temporal**, como en un sistema real: se entrena con el pasado y se evalúa con lo que viene después.

| Split | Fechas | Uso |
|---|---|---|
| `train` | 1 al 5 de marzo | Entrenamiento |
| `test` | 6 de marzo | Evaluación de cada run |
| `nuevas` | 7 de marzo | Transacciones que el modelo registrado puntúa en el notebook 04 |

## Lo mínimo que tenés que experimentar (notebook 02)

- Al menos **5 runs** con configuraciones distintas. Los experimentos sugeridos del notebook cubren las preguntas: la regla sola, los tres conjuntos de variables, los tres modelos, `class_weight = balanced` y un umbral más bajo.
- **Un barrido** de un hiperparámetro (sugerido: `max_depth` en un `random_forest` con `completas`).

Los runs se acumulan en tu experimento: podés volver al 02 cuantas veces quieras. Para comparar, ejecutá después el 03.

## Qué se crea

```text
Tablas:      ml_features (features + etiqueta + split), ml_predictions (scoring del notebook 04)
Experimento: /Users/<tu_usuario>/bigdata_<student_id>_clase05   (Experiments en el menú lateral)
Modelo:      <catálogo>.bigdata_<student_id>.fraud_model con alias champion   (Catalog → tu esquema → Models)
```

Ninguna tabla de las clases anteriores se modifica.

## Preguntas

Las preguntas son cortas. Cuando piden un dato, copiá el valor que te dieron tus notebooks: como cada uno elige sus experimentos, **los números van a variar entre alumnos**. Alcanza con una a tres oraciones por respuesta.

### Datos y tracking (`00_preflight`, `01_primer_run`)

1. ¿Cuántas filas tiene cada split de `ml_features` y qué porcentaje de contracargos hay en cada uno? ¿Por qué se separa por fecha y no al azar?
2. ¿Qué accuracy obtiene un "modelo" que siempre dice que no hay contracargo? ¿Por qué la práctica usa el PR-AUC como métrica principal?
3. ¿Qué quedó registrado en el run `01_manual_logistica` como parámetros, métricas y artefactos? ¿Qué diferencia hay entre un experimento y un run?
4. ¿Cuántos parámetros registró autolog y qué métricas? ¿Qué no registra autolog que sí registramos a mano?
5. ¿Dieron las mismas métricas `01_repro_a` y `01_repro_b`? Nombrá las cuatro cosas que hay que fijar para que un run sea reproducible.
6. ¿Qué pasó al llamar al modelo sin la columna `amount`? ¿Para qué sirve la firma (*signature*) del modelo?

### Tus experimentos (`02_mis_experimentos`)

7. ¿Cuál fue tu mejor run (modelo, variables, hiperparámetros y PR-AUC)? ¿Cuánto mejoró respecto de usar sólo `rule_alert` (`solo_regla`)?
8. Con el mismo modelo, ¿cuánto cambió el PR-AUC al pasar de `basicas` a `cliente` y a `completas`? ¿Qué variables resultaron más importantes en tu mejor run?
9. Con `completas`, ¿qué modelo anduvo mejor: regresión logística, Random Forest o Gradient Boosting? ¿Por qué un modelo de árboles puede aprovechar combinaciones de variables (por ejemplo, de noche *y* por transferencia) que una logística no ve?
10. ¿Qué cambió en precision, recall y cantidad de alertas al usar `class_weight = balanced`? ¿Cambió mucho el PR-AUC?
11. ¿Qué pasó al bajar el umbral? ¿Por qué el PR-AUC no depende del umbral y el F1 sí?
12. ¿Qué hiperparámetro barriste y con qué valor obtuviste el mejor PR-AUC de test? ¿Hubo valores con `train_pr_auc` mucho más alto que el de test? ¿Cómo se llama ese fenómeno?

### Comparar y elegir (`03_comparar_y_elegir`)

13. ¿Coincidieron tu mejor run por PR-AUC y tu mejor run por accuracy? Explicá por qué pueden no coincidir.
14. En el gráfico de PR-AUC de train contra test, ¿qué runs quedan más lejos de la diagonal y qué indica eso?
15. ¿Qué ventaja tiene consultar los runs con `mlflow.search_runs` en lugar de mirarlos en la interfaz? Escribí el `filter_string` que usarías para traer sólo tus Random Forest con PR-AUC de test mayor a 0,55.
16. En fraude, ¿qué cuesta más, una alerta falsa o un contracargo no detectado? Si el equipo de riesgo sólo puede revisar una cantidad fija de alertas por día, ¿cómo usarías el umbral?

### Registro, uso y monitoreo (`04_registro_y_uso`)

17. ¿Se pudo registrar el modelo en Unity Catalog? Indicá nombre, versión y alias (o el error, si falló). ¿Qué ventaja tiene cargar `models:/...@champion` en lugar de `runs:/<run_id>/model`?
18. ¿Cuántas transacciones nuevas se puntuaron y cuántas generaron alerta? ¿Qué columnas de `ml_predictions` permiten auditar cada decisión? ¿Por qué el umbral se guarda fuera del modelo?
19. Cuando llegaron los contracargos, ¿el PR-AUC sobre `nuevas` fue parecido al de test? En la campaña simulada, ¿qué pasó con el porcentaje de alertas? ¿Qué es el drift y por qué se puede detectar antes de tener las etiquetas?

### Cierre

20. Ubicá lo que hiciste en el ciclo de vida de MLOps (datos, entrenamiento, tracking, registro, despliegue, monitoreo). ¿Qué faltaría para tener este modelo en producción real? Nombrá al menos dos cosas.

## Entrega

La publicación, el acceso público y el envío a los profesores siguen el [formato común de entrega](../README.md#formato-común-de-entrega).

La entrega es **un único `README.md`** dentro de `resolucion-practica-5/` en tu repositorio personal:

```text
resolucion-practica-5/
└── README.md
```

El README debe incluir nombre, `student_id` y escala, **la tabla de tus runs** que imprime el notebook 03 (sección 5) y las respuestas a las 20 preguntas. Podés partir de la [plantilla](PLANTILLA_ENTREGA.md). No hace falta exportar los notebooks; si querés, sumá una captura de la comparación de runs en la interfaz de MLflow.

No incluyas datos generados, modelos, credenciales ni tokens.

## Problemas frecuentes

- **`Falta ... silver_transactions`**: ejecutá la clase 2 con el mismo `student_id` y escala.
- **`Falta ml_features`**: ejecutá primero `00_preflight`.
- **El registro en Unity Catalog falla en el notebook 04**: puede pasar por limitaciones de Free Edition. El notebook lo informa y sigue con el modelo del run; respondé la pregunta 17 con el error que apareció.
- **Cambié los widgets pero el run salió con la configuración anterior**: las celdas que entrenan usan lo que muestra la celda "Configuración elegida". Si no se actualizó sola al cambiar los widgets, ejecutala y después volvé a entrenar.
- **El barrido dice que el hiperparámetro no corresponde al modelo**: `C` es sólo de la regresión logística, `n_estimators` sólo del Random Forest y `learning_rate` sólo del Gradient Boosting. Cambiá el modelo o el barrido.
- **No encuentro el modelo en los artefactos del run**: con MLflow 3 los modelos aparecen en la sección **Logged models** del experimento, no en *Artifacts*.
- **Quiero empezar de cero**: volvé a ejecutar `00_preflight` (reconstruye `ml_features`) y, si querés borrar los runs, seleccionalos en la interfaz del experimento y usá **Delete**. Los runs borrados no aparecen en el notebook 03.
- **Con escala `demo` los Random Forest tardan**: usá `small`, o elegí menos árboles y profundidad limitada.
