from __future__ import annotations

from typing import Any

import polars as pd  # type: ignore
from _utils import use_update
from secretset.main import collect_unique_from_df


def test_collect_df_data(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    a, b = df1["a"], df2["a"]
    uniques: set[Any] = set()
    res = set()
    for df in [df1, df2]:
        # update the correct solution
        uniques.update(use_update(df, uniques))

        # update our solution
        res.update(collect_unique_from_df(df, ["a", "b"]))

    assert a == b
    assert uniques == res
