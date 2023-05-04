import polars as pl  # type: ignore
from pytest import fixture  # type: ignore


@fixture
def df1() -> pl.DataFrame:
    return pl.DataFrame({"a": [0, 1, "z"]})


@fixture
def df2() -> pl.DataFrame:
    return pl.DataFrame({"a": [0, 1, "z"], "b": ["blue", "red", "green"]})
