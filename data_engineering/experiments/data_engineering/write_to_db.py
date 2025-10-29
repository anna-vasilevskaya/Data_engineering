#!/usr/bin/env python3

import os
import sys
from pathlib import Path

import pandas as pd
import psycopg2
from loguru import logger
from dotenv import load_dotenv

# Add project root to path for imports
PROJ_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJ_ROOT))

from data_engineering.config import PROCESSED_DATA_DIR

# Load environment variables
load_dotenv()


def get_db_connection():
    """Create database connection using environment variables."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        logger.info("Successfully connected to PostgreSQL database")
        return conn
    except psycopg2.Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise


def create_table_if_not_exists(cursor, table_name):
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
    logger.info(f"Table {table_name} created or already exists")


def insert_data(cursor, table_name, df):
    insert_sql = f"""
    INSERT INTO {table_name} (
        observation_id, common_name, scientific_name, family, genus,
        observed_length_m, observed_weight_kg, age_class, sex,
        date_of_observation, country_region, habitat_type,
        conservation_status, observer_name, notes
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert DataFrame to list of tuples
    data_tuples = []
    for _, row in df.iterrows():
        data_tuples.append(
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
        )

    # make batch insert
    cursor.executemany(insert_sql, data_tuples)
    logger.info(f"Inserted {len(data_tuples)} rows into {table_name}")


def main():
    # environment variables
    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
        "TABLE_NAME",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        logger.error(f"Missing environment variables: {missing_vars}")
        logger.info("Set environment variables - .env file")
        return 1

    table_name = os.getenv("TABLE_NAME")
    data_file = PROCESSED_DATA_DIR / "dataset.parquet"

    if not data_file.exists():
        logger.error(f"Data file not found: {data_file}")
        logger.info("Run import_dataset.py to process the data")
        return 1

    try:
        logger.info(f"Reading from {data_file}")
        df = pd.read_parquet(data_file)

        # Limit max 100 rows
        if len(df) > 100:
            df = df.head(100)
            logger.info(f"Limited to 100 rows")

        logger.info(f"Loaded {len(df)} rows of data")

        # Connect
        conn = get_db_connection()
        cursor = conn.cursor()

        create_table_if_not_exists(cursor, table_name)

        insert_data(cursor, table_name, df)

        # Finish
        conn.commit()
        logger.success(f"Successfully uploaded data to the table")

        cursor.close()
        conn.close()

        return 0

    except Exception as e:
        logger.error(f"Error during data upload: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
