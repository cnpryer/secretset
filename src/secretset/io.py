from __future__ import annotations

from pathlib import Path

import polars as pl


def read_file(filepath: Path) -> pl.DataFrame:
    """Read file from current directory using filepath.
    Args:
        filepath (Path): Filepath. Only reads xlsx, xls, and csv.
    Returns:
        pd.DataFrame: Polars DataFrame
    """
    filename = filepath.name

    if filename.lower().endswith(".xls") or filename.lower().endswith(".xlsx"):
        return pl.read_excel(filepath)

    if filename.lower().endswith(".csv"):
        return pl.read_csv(filepath)

    raise Exception("File must be .xls, .xlsx, .csv.")
