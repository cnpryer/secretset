from __future__ import annotations

from datetime import datetime
from typing import Any

import polars as pl

from secretset.collect import collect_unique_from_df
from secretset.map import map_sequence  # type: ignore


def anonymize_dataframes(
    dataframes: list[pl.DataFrame], columns: list[str]
) -> list[pl.DataFrame]:
    if isinstance(dataframes, pl.DataFrame):
        dataframes = [dataframes]

    # all unique data from the selected fields
    data: set[Any] = set()

    # collect unique data from a df into a set
    for df in dataframes:
        cols = [col for col in columns if col in df.columns]
        data.update(collect_unique_from_df(df, cols))

    # create a dataframe mapping dictionary out of a set of uniques
    mapping = map_sequence(list(data))

    # update each field selected with anonymous data using the mapping
    for i in range(len(dataframes)):
        cols = [col for col in columns if col in dataframes[i].columns]
        dataframes[i] = _anonymize_df(dataframes[i], mapping, cols)

    return dataframes


def _anonymize_df(
    df: pl.DataFrame,
    mapping: dict[str | int | float | datetime, int],
    cols: list[str] | None = None,
) -> pl.DataFrame:
    """This function performs a copy."""
    if cols is None:
        cols = df.columns

    _map = {str(k): str(mapping[k]) for k in mapping}
    _df = (
        df.lazy()
        .with_columns(pl.all().cast(pl.Utf8).map_dict(_map).cast(pl.Int32))
        .collect()
    )

    return _df
