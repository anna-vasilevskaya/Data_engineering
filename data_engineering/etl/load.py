from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from loguru import logger

from .utils import ensure_dir


load_dotenv()


def validate_parquet_written(parquet_path: Path) -> None:
    if not parquet_path.exists():
        raise FileNotFoundError(f"Processed parquet not found: {parquet_path}")


def write_processed_parquet(df: pd.DataFrame, data_root: Path) -> Path:
    processed_dir = data_root / "processed"
    ensure_dir(processed_dir)
    out_path = processed_dir / "dataset.parquet"
    df.to_parquet(out_path, index=False)
    validate_parquet_written(out_path)
    return out_path


def _get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def _create_table_if_not_exists(cursor, table_name: str) -> None:
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        observation_id INT PRIMARY KEY,
        common_name VARCHAR(100),
        scientific_name VARCHAR(100),
        family VARCHAR(50),
        genus VARCHAR(50),
        observed_length_m REAL,
        observed_weight_kg REAL,
        age_class VARCHAR(20),
        sex VARCHAR(10),
        date_of_observation DATE,
        country_region VARCHAR(50),
        habitat_type VARCHAR(50),
        conservation_status VARCHAR(30),
        observer_name VARCHAR(100),
        notes TEXT
    );
    """
    cursor.execute(create_table_sql)


def _insert_rows(cursor, table_name: str, df: pd.DataFrame) -> int:
    insert_sql = f"""
    INSERT INTO {table_name} (
        observation_id, common_name, scientific_name, family, genus,
        observed_length_m, observed_weight_kg, age_class, sex,
        date_of_observation, country_region, habitat_type,
        conservation_status, observer_name, notes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data_tuples = [
        (
            int(row["Observation ID"]),
            str(row["Common Name"]),
            str(row["Scientific Name"]),
            str(row["Family"]),
            str(row["Genus"]),
            float(row["Observed Length (m)"]),
            float(row["Observed Weight (kg)"]),
            str(row["Age Class"]),
            str(row["Sex"]),
            row["Date of Observation"].date(),
            str(row["Country/Region"]),
            str(row["Habitat Type"]),
            str(row["Conservation Status"]),
            str(row["Observer Name"]),
            str(row["Notes"]),
        )
        for _, row in df.iterrows()
    ]
    cursor.executemany(insert_sql, data_tuples)
    return len(data_tuples)


def load_to_db(df: pd.DataFrame, table_name: str) -> int:
    if len(df) > 100:
        df = df.head(100)
        logger.info("Limiting to first 100 rows for DB load")

    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        _create_table_if_not_exists(cursor, table_name)
        count = _insert_rows(cursor, table_name, df)
        conn.commit()
        logger.info(f"Inserted {count} rows into {table_name}")
        return count
    finally:
        try:
            cursor.close()
        finally:
            conn.close()

