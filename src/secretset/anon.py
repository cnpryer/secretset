from __future__ import annotations

from datetime import datetime

import pandas as pd  # type: ignore


def anonymize_df(
    df: pd.DataFrame,
    mapping: dict[str | int | float | datetime, int],
    cols: list[str] | None = None,
) -> pd.DataFrame:
    if cols is None:
        cols = df.columns.tolist()

    for col in cols:
        df = df.replace({col: mapping})

    return df
