from pathlib import Path

from loguru import logger
from tqdm import tqdm
import typer

from data_engineering.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from data_engineering.data_loader import load_and_process_dataset

app = typer.Typer()


@app.command()
def main(
    # default paths
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.parquet",
):
    logger.info(f"Reading dataset from {input_path}")

    raw_data = load_and_process_dataset(str(input_path))

    logger.info(f"Saving processed dataset to {output_path}")
    raw_data.to_parquet(output_path, index=False)
    logger.success("Processing dataset complete.")


if __name__ == "__main__":
    app()
