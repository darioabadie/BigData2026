# Databricks notebook source
"""Reglas reutilizables de calidad para transacciones Silver."""

from pyspark.sql import functions as F


ALLOWED_PAYMENT_CHANNELS = ("card", "wallet", "transfer")


def add_transaction_types(frame):
    """Conserva campos raw y agrega una representación tipada."""
    return (
        frame
        .withColumn("transaction_id_typed", F.expr("try_cast(transaction_id AS BIGINT)"))
        .withColumn("customer_id_typed", F.expr("try_cast(customer_id AS BIGINT)"))
        .withColumn("product_id_typed", F.expr("try_cast(product_id AS BIGINT)"))
        .withColumn("event_ts_typed", F.expr("try_cast(event_ts AS TIMESTAMP)"))
        .withColumn("amount_typed", F.expr("try_cast(amount AS DECIMAL(12,2))"))
        .withColumn("is_fraud_typed", F.expr("try_cast(is_fraud AS INT)"))
        .withColumn("updated_at_typed", F.expr("try_cast(updated_at AS TIMESTAMP)"))
    )


def add_quality_reason(frame):
    """Asigna una causa principal de rechazo; NULL significa registro válido."""
    allowed = list(ALLOWED_PAYMENT_CHANNELS)
    return frame.withColumn(
        "quality_reason",
        F.when(F.col("transaction_id_typed").isNull(), F.lit("INVALID_TRANSACTION_ID"))
        .when(F.col("customer_id_typed").isNull(), F.lit("INVALID_CUSTOMER_ID"))
        .when(F.col("product_id_typed").isNull(), F.lit("INVALID_PRODUCT_ID"))
        .when(F.col("event_ts_typed").isNull(), F.lit("INVALID_EVENT_TS"))
        .when(F.col("amount_typed").isNull() | (F.col("amount_typed") <= 0), F.lit("INVALID_AMOUNT"))
        .when(F.col("payment_channel").isNull() | ~F.col("payment_channel").isin(allowed), F.lit("INVALID_PAYMENT_CHANNEL"))
        .when(F.col("is_fraud_typed").isNull() | ~F.col("is_fraud_typed").isin([0, 1]), F.lit("INVALID_FRAUD_FLAG"))
        .when(F.col("updated_at_typed").isNull(), F.lit("INVALID_UPDATED_AT"))
        .when(F.col("known_customer").isNull(), F.lit("UNKNOWN_CUSTOMER"))
        .when(F.col("known_product").isNull(), F.lit("UNKNOWN_PRODUCT")),
    )

