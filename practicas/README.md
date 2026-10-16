# Prácticas integradas — Herramientas de procesamiento para grandes volúmenes de datos

Estas prácticas usan un único caso conductor: una plataforma ficticia de comercio electrónico que necesita detectar operaciones potencialmente fraudulentas. Cada encuentro agrega una capa al mismo sistema.

## Recorrido

1. **Clase 1 — Ingesta y Bronze:** workspace, Unity Catalog, PySpark, CSV/JSON, Parquet y Delta.
2. **Clase 2 — Silver y Gold:** calidad, deduplicación, joins, `MERGE` y productos analíticos.
3. **Clase 3 — NoSQL:** CAP y PACELC, clave-valor, documental, grafos, vectorial y columnar sobre los mismos datos Silver.
4. **Clase 4 — Streaming:** log y offsets, ingesta incremental, ventanas y watermarks, garantías de entrega y CDC.
5. **Clase 5 — MLOps con MLflow:** tracking de experimentos, comparación de modelos, registro con alias, inferencia batch y monitoreo.

Las clases 1 a 5 están implementadas sobre Databricks Free Edition. La segunda continúa directamente desde las tablas Bronze construidas en la primera; la tercera reorganiza las tablas Silver según los modelos NoSQL; la cuarta usa las dimensiones Silver para demostrar los conceptos de streaming con llegadas controladas, y la quinta entrena modelos de contracargos sobre las tablas Silver y los gestiona con MLflow.

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

Los archivos crudos se guardan en un volumen administrado llamado `landing`. Las capas del recorrido integrado usan `bronze_*`, `silver_*` y `gold_*`; la clase 3 usa `nosql_*`, la clase 4 usa `stream_*` y la clase 5 usa `ml_*`.

## Formato común de entrega

Las entregas se publican en el repositorio personal `mi-primer-proyecto` de la [guía de Git y GitHub](GUIA_GIT_GITHUB.md), bajo `resolucion-practica-1/`, `resolucion-practica-2/`, `resolucion-practica-3/`, `resolucion-practica-4/` o `resolucion-practica-5/`, según la clase.

Todas incluyen un `README.md` con nombre, `student_id`, escala, resultados y respuestas requeridas, más los notebooks solicitados exportados con sus salidas. Para análisis, adjuntá consulta SQL o PySpark, resultado relevante e interpretación; para preguntas sobre código, identificá notebook/helper y sección. Si una exportación no conserva las salidas, adjuntá capturas legibles de la ejecución.

El repositorio debe ser público y accesible desde una ventana privada. Enviá su URL a **dabadie@itba.edu.ar** y **ghenrion@itba.edu.ar**. No publiques credenciales, checkpoints ni archivos generados del volumen.

Cada TP define sus archivos obligatorios, preguntas, visualizaciones y desafíos. La clase 1 tiene una entrega introductoria y desafío opcional; la clase 2 incluye 20 preguntas y cuatro visualizaciones; las clases 3 y 4 tienen notebooks demostrativos y una entrega de 20 preguntas cortas; la clase 5 suma experimentos propios con widgets, una tabla de runs y 20 preguntas cortas.

## Uso de la clase 1

Ejecutar en orden:

1. `GUIA_SETUP_DATABRICKS_FREE.md`
2. `clase-01/00_setup.ipynb`
3. `clase-01/01_ingesta_bronze.ipynb`
4. `clase-01/02_desafio.ipynb`

El desafío es opcional para la entrega de clase 1. Este directorio todavía no incluye una solución docente publicada.

## Uso de la clase 2

Conservá el mismo `student_id` y la misma escala de la clase 1. Luego ejecutá:

1. `clase-02/00_preflight.ipynb`
2. `clase-02/00_generate_new_batch.ipynb`
3. La secuencia de cuatro notebooks mediante el Job descripto en `clase-02/GUIA_CREAR_JOB.md`
4. `clase-02/05_visualizacion.ipynb`, una vez validado el pipeline

La práctica construye Silver y Gold, incorpora cuarentena y `MERGE`, y valida la llegada de un archivo nuevo y la reejecución idempotente del pipeline.

## Uso de la clase 3

Conservá el mismo `student_id` y escala de la clase 2. Seguí el [TP de NoSQL](clase-03/README.md): `00_preflight` y luego los notebooks `01` a `06`, uno por modelo (CAP/PACELC, clave-valor, documental, grafos, vectorial y columnar). Son demostrativos: se ejecutan celda por celda sin modificar código y no tocan las tablas de las clases anteriores.

La entrega es un `README.md` en `resolucion-practica-3/` con las respuestas a 20 preguntas cortas. Hay una [plantilla](clase-03/PLANTILLA_ENTREGA.md).

## Uso de la clase 4

Conservá el mismo `student_id` y escala de la clase 2. Seguí el [TP de streaming](clase-04/README.md): `00_preflight` y luego los notebooks `01` a `05` (log y offsets, ingesta y enriquecimiento, tiempo y ventanas, garantías y fallas, CDC). Son demostrativos: se ejecutan celda por celda sin modificar código, cada uno reinicia sólo sus propias tablas `stream_*` y no hace falta crear un Job.

La entrega es un `README.md` en `resolucion-practica-4/` con las respuestas a 20 preguntas cortas. Hay una [plantilla](clase-04/PLANTILLA_ENTREGA.md).

## Uso de la clase 5

Conservá el mismo `student_id` y escala de la clase 2. Seguí el [TP de MLOps](clase-05/README.md): `00_preflight` arma la tabla `ml_features` y tu experimento de MLflow; `01` muestra qué registra un run; en `02` hacés **tus propios experimentos** eligiendo modelo, variables e hiperparámetros con widgets (sin escribir código); `03` compara tus runs y `04` registra el mejor en Unity Catalog, lo usa para puntuar transacciones nuevas y lo monitorea.

La entrega es un `README.md` en `resolucion-practica-5/` con la tabla de tus runs y las respuestas a 20 preguntas cortas. Hay una [plantilla](clase-05/PLANTILLA_ENTREGA.md).

## Reinicio seguro

Los módulos comparten el esquema personal y el volumen `landing`. Eliminar ese esquema con `DROP SCHEMA ... CASCADE` elimina recursos de todos los TPs del alumno, incluidos datos y checkpoints de streaming; no es un reinicio aislado de clase 1.

El setup no ejecuta esa eliminación automáticamente. Para repetir una etapa, seguí las instrucciones del TP: algunas reconstruyen tablas derivadas; los notebooks de las clases 3 y 4 reinician sólo sus propias tablas al volver a ejecutarse. No cambies la escala de clases 1–4 dentro de un experimento existente. No se debe borrar el catálogo ni esquemas ajenos.

## Revisión del material

La [revisión de consistencia del 7 de octubre de 2026](REVISION_CONSISTENCIA.md) registra las correcciones realizadas y una inconsistencia pendiente en la interpretación del resumen por lote de clase 2.
