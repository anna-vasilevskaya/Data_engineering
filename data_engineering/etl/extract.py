from __future__ import annotations

from pathlib import Path
from typing import Literal, Iterable, Optional


import pandas as pd

from .utils import ensure_dir


REQUIRED_COLUMNS: list[str] = [
    "Observation ID",
    "Common Name",
    "Scientific Name",
    "Family",
    "Genus",
    "Observed Length (m)",
    "Observed Weight (kg)",
    "Age Class",
    "Sex",
    "Date of Observation",
    "Country/Region",
    "Habitat Type",
    "Conservation Status",
    "Observer Name",
    "Notes",
]

def _detect_format(source: Path | str) -> Literal["csv", "parquet", "unknown"]:
    s = str(source).lower()
    if s.endswith(".csv"):  # simple heuristic
        return "csv"
    if s.endswith(".parquet") or s.endswith(".pq"):
        return "parquet"
    return "unknown"


def validate_required_columns(df: pd.DataFrame, required: Optional[Iterable[str]] = None) -> None:
    expected = set(required or REQUIRED_COLUMNS)
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_non_empty(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("Input dataframe is empty")


def load_raw(source: str | Path) -> pd.DataFrame:
    fmt = _detect_format(source)
    if fmt == "csv":
        df = pd.read_csv(source)
    elif fmt == "parquet":
        df = pd.read_parquet(source)
    else:
        # let pandas try best-effort (URLs, GDrive links with query id, etc.)
        df = pd.read_csv(source)

    validate_non_empty(df)
    validate_required_columns(df)
    return df


def persist_raw_csv(df: pd.DataFrame, data_root: Path) -> Path:
    raw_dir = data_root / "raw"
    ensure_dir(raw_dir)
    out_path = raw_dir / "dataset.csv"
    df.to_csv(out_path, index=False)
    return out_path

   