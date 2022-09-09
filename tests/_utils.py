from __future__ import annotations

import pandas as pd  # type: ignore


def use_update(df: pd.DataFrame, _set: set) -> set:
    """The result of collect_df_data should always be the same
    as the result of using set.update().

    Args:
        df (pd.DataFrame): DataFrame to collect data from.
        _set (set): Set to update.

    Returns:
        set: Updated set.
    """
    for values in df.values:
        _set.update(list(values))

    return _set
