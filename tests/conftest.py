import pandas as pd  # type: ignore
from pytest import fixture


@fixture
def df1() -> pd.DataFrame:
    return pd.DataFrame({"a": [0, 1, "z"]})


@fixture
def df2() -> pd.DataFrame:
    return pd.DataFrame({"a": [0, 1, "z"], "b": ["blue", "red", "green"]})
