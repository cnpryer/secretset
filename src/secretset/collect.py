from __future__ import annotations

from datetime import datetime

import pandas as pd  # type: ignore


def collect_df_data(
    df: pd.DataFrame,
    _set: set[str | int | float | datetime],
    cols: list[str] | None = None,
) -> set:
    """Collect all unique data into a provided set.

    Args:
        df (pd.DataFrame): Pandas DataFrame to collect data from.
        _set (set): Set to update.
        cols (list, optional): Columns to collect data from. Defaults to
            list([]).

    Returns:
        set: Updated set of unique df data.
    """
    if cols is None:
        cols = df.columns.tolist()

    for col in cols:
        _set.update(df[col].tolist())

    return _set
