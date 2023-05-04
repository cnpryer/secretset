from __future__ import annotations

from datetime import datetime

import polars as pl  # type: ignore


def anonymize_df(
    df: pl.DataFrame,
    mapping: dict[str | int | float | datetime, int],
    cols: list[str] | None = None,
) -> pl.DataFrame:
    """This function performs a copy."""
    if cols is None:
        cols = df.columns

    _df = df.clone()

    statement = [pl.col(col).map_dict(mapping) for col in cols]
    if statement:
        _df = df.lazy().with_columns(statement).collect()

    return _df
