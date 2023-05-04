from __future__ import annotations

import polars as pl


def use_update(df: pl.DataFrame, _set: set) -> set:
    """The result of collect_df_data should always be the same
    as the result of using set.update().

    Args:
        df (pd.DataFrame): DataFrame to collect data from.
        _set (set): Set to update.

    Returns:
        set: Updated set.
    """
    _df_data: set = set()
    for col in df.columns:
        _df_data.update(df.lazy().select(pl.col(col).unique()).collect())

    return _set
