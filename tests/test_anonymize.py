from __future__ import annotations

from datetime import datetime

import polars as pl  # type: ignore
from _utils import use_update
from secretset.anon import anonymize_df


def test_anonymize_df(df1: pl.DataFrame, df2: pl.DataFrame) -> None:
    a1, a2 = df1["a"], df2["a"]
    _set: set[int | str | float | datetime] = set()
    _set.update(use_update(df1[["a"]], _set))
    _set.update(use_update(df2[["a"]], _set))

    mapping = {v: i for (i, v) in enumerate(_set)}
    res_1, res_2 = (
        anonymize_df(df1[["a"]].clone(), mapping),
        anonymize_df(df2[["a"]].clone(), mapping),
    )

    old_df = df2
    new_df = df2.clone()
    _set = set()

    for col in old_df.columns:
        _set.update(old_df[col])

    mapping = {v: i for (i, v) in enumerate(_set)}
    new_df = anonymize_df(new_df, mapping)

    assert a1 == a2
    assert res_1.frame_equal(res_2)
    assert not df1[["a"]].frame_equal(res_1)
    assert not df2[["a"]].frame_equal(res_2)
    assert not old_df.frame_equal(new_df)
