from __future__ import annotations

from datetime import datetime
from typing import Sequence


def map_sequence(
    sequence: Sequence[str | int | float | datetime],
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
    unique_data = set(sequence)
    res = {_: i for i, _ in enumerate(unique_data)}

    return res
