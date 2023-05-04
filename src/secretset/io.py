from __future__ import annotations

from pathlib import Path

import polars as pl


def read_file(file_path: Path) -> pl.DataFrame:
    """Read file from current directory using file_path.
    Args:
        file_path (Path): file_path. Only reads xlsx, xls, and csv.
    Returns:
        pd.DataFrame: Polars DataFrame
    """
    match file_path.suffix.lower():
        case ".csv":
            return pl.read_csv(file_path)
        case ".xlsx" | ".xls":
            return pl.read_excel(file_path)
        case ".parquet":
            return pl.read_parquet(file_path)

    raise Exception("File must be .xls, .xlsx, .csv., .parquet")


def write_file(
    df: pl.DataFrame, path: Path, format: str = "csv"
) -> pl.DataFrame:
    match format.lstrip("."):
        case "csv":
            return df.write_csv(path)
        case "parquet":
            return df.write_parquet(path)

    raise Exception("Format must be .csv or .parquet")
