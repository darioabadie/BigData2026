# Prácticas integradas — Herramientas de procesamiento para grandes volúmenes de datos

Estas prácticas usan un único caso conductor: una plataforma ficticia de comercio electrónico que necesita detectar operaciones potencialmente fraudulentas. Cada encuentro agrega una capa al mismo sistema.

## Recorrido

1. **Clase 1 — Ingesta y Bronze:** workspace, Unity Catalog, PySpark, CSV/JSON, Parquet y Delta.
2. **Clase 2 — Silver y Gold:** calidad, deduplicación, joins, `MERGE`, Time Travel y productos analíticos.
3. **Clase 3 — Streaming:** procesamiento incremental, ventanas, watermarks y checkpoints.
4. **Clase 4 — MLOps:** features, MLflow, registro, scoring y monitoreo.

Las clases 1 y 2 están implementadas sobre Databricks Free Edition. La segunda continúa directamente desde las tablas Bronze construidas en la primera.

## Empezar desde cero

Si es tu primer contacto con Git y GitHub, empezá por la [guía básica de Git y GitHub](GUIA_GIT_GITHUB.md). La Parte 1 incluye los conceptos esenciales y un ejercicio desde el navegador; la Parte 2 permite clonar ese repositorio en tu computadora, crear un archivo Markdown y practicar `add`, `commit` y `push`.

Si todavía no tenés el entorno preparado, seguí primero la [guía paso a paso de Databricks Free Edition](GUIA_SETUP_DATABRICKS_FREE.md). Incluye creación de cuenta, GitHub, compute serverless, verificación de Unity Catalog, importación manual y resolución de problemas.

## Requisitos

- Una cuenta personal de Databricks Free Edition.
- Un Git folder conectado a este repositorio, o los notebooks importados manualmente.
- Python y SQL. No se requieren librerías externas.

Free Edition utiliza compute serverless y tiene cuotas diarias. Todos los notebooks incluyen un modo `small` y evitan procesos que queden ejecutándose indefinidamente.

## Convenciones

Cada alumno trabaja en un esquema propio dentro del catálogo predeterminado:

```text
<catalogo_actual>.bigdata_<identificador>
```

Los archivos crudos se guardan en un volumen administrado llamado `landing`, y las tablas siguen la nomenclatura `bronze_*`, `silver_*` y `gold_*`.

## Uso de la clase 1

Ejecutar en orden:

1. `GUIA_SETUP_DATABRICKS_FREE.md`
2. `clase-01/00_setup.ipynb`
3. `clase-01/01_ingesta_bronze.ipynb`
4. `clase-01/02_desafio.ipynb`

El material resuelto se encuentra bajo `clase-01/docente/` y no debería compartirse antes de finalizar la práctica.

## Uso de la clase 2

Conservá el mismo `student_id` y la misma escala de la clase 1. Luego ejecutá:

1. `clase-02/00_preflight.ipynb`
2. `clase-02/00_generate_new_batch.ipynb`
3. La secuencia de cuatro notebooks mediante el Job descripto en `clase-02/GUIA_CREAR_JOB.md`
4. `clase-02/05_visualizacion.ipynb`, una vez validado el pipeline

La práctica construye Silver y Gold, incorpora cuarentena y `MERGE`, y valida la llegada de un archivo nuevo y la reejecución idempotente del pipeline.

## Reinicio seguro

Los notebooks están diseñados para poder ejecutarse más de una vez. El setup muestra, pero no ejecuta automáticamente, la sentencia necesaria para eliminar el esquema personal. No se debe borrar el catálogo ni esquemas ajenos.
