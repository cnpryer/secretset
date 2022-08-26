from secretset.map import map_sequence


def test_map_sequence() -> None:
    sequence = ("A", "A", "B", "C")
    res = map_sequence(sequence)

    assert len(res) == len(set(sequence))
    assert sorted(res) == sorted({"A": 0, "B": 1, "C": 2})
