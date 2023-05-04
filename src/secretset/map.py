from __future__ import annotations

from datetime import datetime
from typing import Sequence

import polars as pl


def map_sequence(
    sequence: Sequence[str | int | float | datetime]
    | set[str | int | float | datetime],
) -> dict[str | int | float | datetime, int]:
    """Anonymize input data using integer ranges for unique data.

    Example:
        ```py
        >> sequence
        ("A", "B", "C")
        >> anonymous_data_map(sequence)
        {"A": 0, "B": 1, "C": 2}
        ```

    Args:
        sequence (Sequence[str | int | float | datetime]): Sequence of data to
            create mapping for.

    Returns:
        dict[int, str | int | float | datetime]: Mapping of input to anonymous
            output data.
    """
    series = pl.Series("source", sequence)

    df = (
        pl.DataFrame(series)
        .lazy()
        .with_columns(
            [
                pl.col("source"),
                pl.arange(0, pl.arange(0, pl.col("source").len())),
            ]
        )
        .collect()
    )
    res = {}
    for pair in df.to_dicts():
        res[pair["source"]] = pair["anon"]

    return res
