from __future__ import annotations

from datetime import datetime

import pandas as pd  # type: ignore
from _utils import use_update

from secretset.main import collect_df_data


def test_collect_df_data(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    a, b = df1["a"].tolist(), df2["a"].tolist()
    uniques: set[int | str | float | datetime] = set()
    res: set[int | str | float | datetime] = set()
    for df in [df1, df2]:
        # update the correct solution
        _uniques = use_update(df, uniques)
        uniques.update(_uniques)

        # update our solution
        _res = collect_df_data(df, res)
        res.update(_res)

    assert a == b
    assert uniques == res
