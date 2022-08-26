from __future__ import annotations

from datetime import datetime
from typing import Sequence

DataTypes = str | int | float | datetime


def map_sequence(inputs: Sequence[DataTypes]) -> dict[DataTypes, int]:
    """Anonymize input data using integer ranges for unique data.
    Example:
    ```
    >> inputs
    ("A", "B", "C")
    anonymous_data_map(inputs)
    >> {"A": 0, "B": 1, "C": 2}
    ```
    Args:
        inputs (Sequence[DataTypes]): Unique data to create
        mapping for.
    Returns:
        dict[int, DataTypes]: Mapping of input to anonymous output data.
    """
    res = {_: i for i, _ in enumerate(inputs)}

    assert len(res) == len(inputs), "Inputs and unique data size don't match."

    return res
