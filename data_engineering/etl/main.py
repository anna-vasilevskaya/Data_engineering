from __future__ import annotations

import argparse
from pathlib import Path
from loguru import logger

from .extract import load_raw, persist_raw_csv
from .transform import cast_schema
from .load import load_to_db, write_processed_parquet
from .utils import ensure_dir


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def data_root() -> Path:
    return repo_root() / "data"


def run_etl(source: str, table_name: str | None, no_db: bool = False) -> None:
    ensure_dir(data_root())

    logger.info("Extract: loading raw source")
    raw_df = load_raw(source)
    raw_csv_path = persist_raw_csv(raw_df, data_root())
    logger.info(f"Raw CSV saved to: {raw_csv_path}")

    logger.info("Transform: casting schema")
    df = cast_schema(raw_df)

    logger.info("Load: writing parquet to data/processed")
    parquet_path = write_processed_parquet(df, data_root())
    logger.info(f"Parquet saved to: {parquet_path}")

    if not no_db and table_name:
        logger.info(f"Load: writing up to 100 rows into DB table '{table_name}'")
        load_to_db(df, table_name)
    else:
        logger.info("DB load skipped")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run ETL pipeline: extract -> transform -> load",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path or URL to source dataset (.csv or .parquet)",
    )
    parser.add_argument(
        "--table-name",
        help="Target DB table name (required to enable DB load)",
    )
    parser.add_argument(
        "--no-db",
        action="store_true",
        help="Do not load into DB",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_etl(source=args.source, table_name=args.table_name, no_db=args.no_db)


if __name__ == "__main__":
    main()
