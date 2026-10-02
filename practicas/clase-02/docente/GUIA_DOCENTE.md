# Guía docente — Práctica 2

## Idea central

La práctica no busca solamente producir tablas Silver y Gold. El objetivo es que los alumnos puedan explicar y demostrar cuatro propiedades: incrementalidad, idempotencia, observabilidad y reconciliación.

## Preparación

1. Ejecutar la práctica 1 con `student_id=docente02` y escala `test`.
2. Ejecutar `00_preflight`.
3. Crear `batch_002` una sola vez.
4. Construir el Job con cuatro tareas y parámetros.
5. Ejecutarlo dos veces y revisar `pipeline_run_audit`.
6. Ejecutar el ejemplo de `05_visualizacion` y verificar que la agregación se realiza en Spark.

## Invariantes esperados

- `bronze_transactions_incremental` contiene filas de `batch_002`.
- `silver_transactions` tiene una sola fila por `transaction_id`.
- La transacción `42` pertenece al lote nuevo y tiene importe `1999.99`.
- `silver_transactions_quarantine` contiene al menos `INVALID_AMOUNT` y `UNKNOWN_CUSTOMER` para el lote.
- La suma y la cantidad de `gold_daily_sales` reconcilian con Silver.
- `gold_batch_summary` contiene aceptados y rechazados para el lote.
- La segunda ejecución mantiene las mismas métricas de negocio.

No fijar cantidades absolutas salvo los dos rechazos controlados: el número de altas válidas depende de la escala.

## Preguntas para la puesta en común

1. ¿Por qué `COPY INTO` no reemplaza la deduplicación por clave de negocio?
2. ¿Qué diferencia existe entre un archivo duplicado y una transacción duplicada?
3. ¿Por qué una tabla de cuarentena es mejor que descartar filas?
4. ¿Cuándo conviene reconstruir Gold y cuándo conviene actualizarla incrementalmente?
5. ¿Qué observabilidad ofrece el Job que no ofrece ejecutar notebooks manualmente?
6. ¿Qué diferencia hay entre describir un gráfico y responder la pregunta que lo motivó?

## Evaluación de visualizaciones

No evaluar solamente la estética. Cada respuesta debe usar la métrica correcta, mantener visible el denominador cuando compara fraude o calidad, elegir un gráfico adecuado y formular una conclusión respaldada por la evidencia. Penalizar el promedio directo de tasas ya agregadas y la conversión de tablas Silver completas a Pandas.

## Extensiones opcionales

- Cambiar el Job a un trigger por llegada de archivos.
- Agregar una rama condicional cuando no haya filas nuevas.
- Incorporar otra regla de calidad con un código propio.
- Crear una visualización sobre `gold_daily_sales`.

Los triggers automáticos y Auto Loader se retomarán formalmente en la clase 3.

