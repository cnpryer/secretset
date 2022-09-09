from __future__ import annotations

from datetime import datetime

import pandas as pd  # type: ignore
from _utils import use_update

from secretset.anon import anonymize_df


def test_anonymize_df(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    a1, a2 = df1["a"].tolist(), df2["a"].tolist()
    _set: set[int | str | float | datetime] = set()
    _set.update(use_update(df1[["a"]], _set))
    _set.update(use_update(df2[["a"]], _set))

    mapping = {v: i for (i, v) in enumerate(_set)}
    res_1, res_2 = (
        anonymize_df(df1[["a"]].copy(), mapping),
        anonymize_df(df2[["a"]].copy(), mapping),
    )

    old_df = df2
    new_df = df2.copy()
    _set = set()

    for col in old_df.columns:
        _set.update(old_df[col].tolist())

    mapping = {v: i for (i, v) in enumerate(_set)}
    new_df = anonymize_df(new_df, mapping)

    assert a1 == a2
    assert res_1.equals(res_2)
    assert not df1[["a"]].equals(res_1)
    assert not df2[["a"]].equals(res_2)
    assert not old_df.equals(new_df)
