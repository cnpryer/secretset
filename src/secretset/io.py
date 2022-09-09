from __future__ import annotations

from pathlib import Path

import pandas as pd  # type: ignore


def read_file(filepath: Path) -> pd.DataFrame:
    """Read file from current directory using filepath.
    Args:
        filepath (Path): Filepath. Only reads xlsx, xls, and csv.
    Returns:
        pd.DataFrame: Pandas DataFrame
    """
    filename = filepath.name

    if filename.lower().endswith(".xls") or filename.lower().endswith(".xlsx"):
        return pd.read_excel(filepath)

    if filename.lower().endswith(".csv"):
        return pd.read_csv(filepath)

    raise Exception("File must be .xls, .xlsx, .csv.")
