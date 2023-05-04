from __future__ import annotations

from typing import Any, Sequence

import polars as pl


def collect_unique_from_df(
    df: pl.DataFrame,
    cols: Sequence[str] | None = None,
) -> set:
    """Collect all unique data into a provided set.

    Args:
        df (pl.DataFrame): Polars DataFrame to collect data from.
        cols (list, optional): Columns to collect data from. Defaults to
            list([]).

    Returns:
        set: Updated set of unique df data.
    """
    if cols is None:
        cols = df.columns

    _set: set[Any] = set()

    for col in cols:
        _set.update(
            (
                v
                for v in df.lazy()
                .select(pl.col(col).unique())
                .collect()
                .iter_rows()
            )
        )

    return _set
