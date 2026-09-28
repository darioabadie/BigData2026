# Clase práctica 2 — Silver, Gold y orquestación

## Propósito

Transformar las tablas Bronze de la práctica 1 en datos confiables y productos analíticos. El flujo se ejecuta como un Lakeflow Job, admite archivos nuevos y demuestra idempotencia mediante validaciones automáticas.

## Objetivos

- Aplicar contratos de tipos y reglas de calidad.
- Separar registros válidos de una cuarentena explicable.
- Resolver duplicados y correcciones con `MERGE`.
- Construir tablas Gold con un grano de negocio explícito.
- Orquestar notebooks dependientes con Lakeflow Jobs.
- Probar una carga nueva sin cambiar el código del pipeline.
- Verificar reconciliación e idempotencia.

## Requisitos previos

La práctica 1 debe haber creado, en el mismo esquema:

```text
bronze_customers
bronze_products
bronze_transactions
bronze_events
```

Usá en todos los notebooks el mismo `student_id` y la misma escala de la práctica 1. Si trabajaste con `small`, no cambies a `test`: las claves foráneas se generan de acuerdo con la escala.

## Secuencia

1. Ejecutá `00_preflight.ipynb`.
2. Ejecutá manualmente `00_generate_new_batch.ipynb` con `batch_002`.
3. Creá el Job siguiendo `GUIA_CREAR_JOB.md`.
4. Ejecutá el Job con `expected_batch_id=batch_002`.
5. Revisá las cuatro tareas y las tablas resultantes.
6. Ejecutá nuevamente el mismo Job sin crear otro archivo.
7. Confirmá que la segunda validación informa métricas estables.
8. Ejecutá manualmente `05_visualizacion.ipynb` y resolvé las cuatro preguntas usando las tablas Gold.

## Tablas resultantes

```text
bronze_transactions_incremental
bronze_transactions_all       (vista)
silver_customers
silver_products
silver_transactions
silver_transactions_quarantine
gold_daily_sales
gold_customer_risk
gold_batch_summary
pipeline_run_audit
```

## Duración estimada

| Bloque | Minutos |
|---|---:|
| Repaso y preflight | 15 |
| Contratos, calidad y cuarentena | 25 |
| Silver y `MERGE` | 30 |
| Pausa | 10 |
| Gold y reconciliación | 25 |
| Construcción del Job | 25 |
| Archivo nuevo y primera ejecución | 20 |
| Segunda ejecución y cierre | 10 |
| Visualización orientada a preguntas | 20 |

## Entrega

En tu repositorio personal creá `resolucion-practica-2/` con:

```text
resolucion-practica-2/
├── README.md
├── 02_build_silver.ipynb
├── 03_build_gold.ipynb
├── 04_validate_pipeline.ipynb
└── 05_visualizacion.ipynb
```

El `README.md` debe incluir:

- Nombre y `student_id`.
- Captura del DAG del Job con las cuatro tareas.
- URL del Job o su nombre exacto.
- Resultados de la primera y segunda ejecución.
- Cantidades aceptadas y rechazadas para `batch_002`.
- Explicación breve de por qué `COPY INTO` y `MERGE` resuelven problemas diferentes.
- Explicación del grano de cada tabla Gold.
- Las cuatro visualizaciones y una respuesta explícita para cada pregunta.

No incluyas datos, credenciales ni tokens.

