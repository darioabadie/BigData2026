# Databricks notebook source
"""Genera lotes incrementales pequeños y reproducibles para la práctica 2."""

from datetime import datetime, timedelta
from decimal import Decimal
import csv
import io
import re


BATCH_ROWS = {"test": 20, "small": 200, "demo": 1_000}


def normalize_batch_id(value: str) -> str:
    """Valida un identificador utilizable en datos y nombres de archivo."""
    normalized = value.strip().lower()
    if not re.fullmatch(r"batch_[0-9]{3,6}", normalized):
        raise ValueError("Usá el formato batch_002, batch_003, etc.")
    return normalized


def _batch_number(batch_id: str) -> int:
    return int(batch_id.split("_")[1])


def build_incremental_rows(config, batch_id: str) -> list[dict[str, str]]:
    """Crea altas, una corrección, un duplicado y dos errores controlados."""
    batch_id = normalize_batch_id(batch_id)
    number = _batch_number(batch_id)
    row_count = BATCH_ROWS[config.scale]
    start_id = config.rows["transactions"] + number * (row_count + 10)
    base_time = datetime(2026, 3, 8) + timedelta(days=number)
    rows = []

    for index in range(row_count):
        event_time = base_time + timedelta(seconds=index * 37)
        amount = Decimal("10.00") + Decimal((index * 791 + number * 101) % 150000) / Decimal("100")
        channel = ["card", "wallet", "transfer"][index % 3]
        rows.append(
            {
                "transaction_id": str(start_id + index),
                "customer_id": str((index * 17 + number) % config.rows["customers"]),
                "product_id": str((index * 13 + number) % config.rows["products"]),
                "event_ts": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                "amount": f"{amount:.2f}",
                "payment_channel": channel,
                "device_id": f"device_incremental_{(index + number) % max(10, config.rows['customers'] // 2)}",
                "is_fraud": "1" if amount > Decimal("1300") else "0",
                "source_batch_id": batch_id,
                "updated_at": (event_time + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    # Corrección de una transacción histórica existente.
    rows.append(
        {
            "transaction_id": "42",
            "customer_id": "0",
            "product_id": "0",
            "event_ts": base_time.strftime("%Y-%m-%d %H:%M:%S"),
            "amount": "1999.99",
            "payment_channel": "card",
            "device_id": "device_corrected_42",
            "is_fraud": "1",
            "source_batch_id": batch_id,
            "updated_at": (base_time + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    # El mismo registro de negocio llega dos veces en el archivo.
    rows.append(rows[0].copy())

    invalid_amount = rows[1].copy()
    invalid_amount.update(
        {
            "transaction_id": str(start_id + row_count),
            "amount": "N/A",
            "source_batch_id": batch_id,
        }
    )
    rows.append(invalid_amount)

    unknown_customer = rows[2].copy()
    unknown_customer.update(
        {
            "transaction_id": str(start_id + row_count + 1),
            "customer_id": str(config.rows["customers"] + 999),
            "source_batch_id": batch_id,
        }
    )
    rows.append(unknown_customer)
    return rows


def rows_to_csv(rows: list[dict[str, str]]) -> str:
    """Serializa el lote con cabecera estable."""
    if not rows:
        raise ValueError("El lote no puede estar vacío")
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue()


def incremental_file_path(config, batch_id: str) -> str:
    batch_id = normalize_batch_id(batch_id)
    return f"{config.volume_path}/incoming/transactions/transactions_{batch_id}.csv"


def write_incremental_batch(dbutils, config, batch_id: str) -> dict:
    """Deposita un archivo nuevo; nunca sobrescribe silenciosamente un lote."""
    batch_id = normalize_batch_id(batch_id)
    rows = build_incremental_rows(config, batch_id)
    path = incremental_file_path(config, batch_id)
    parent = path.rsplit("/", 1)[0]
    dbutils.fs.mkdirs(parent)

    try:
        existing = {item.path.removeprefix("dbfs:").rstrip("/") for item in dbutils.fs.ls(parent)}
    except Exception:
        existing = set()
    if path in existing:
        raise FileExistsError(
            f"{path} ya existe. Elegí el siguiente batch_id; no sobrescribas una entrada procesada."
        )

    dbutils.fs.put(path, rows_to_csv(rows), overwrite=False)
    distinct_ids = len({row["transaction_id"] for row in rows})
    return {
        "batch_id": batch_id,
        "path": path,
        "physical_rows": len(rows),
        "distinct_transaction_ids": distinct_ids,
        "expected_invalid_rows": 2,
        "contains_historical_correction": True,
    }

