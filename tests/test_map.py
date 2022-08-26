from secretset.map import map_sequence


def test_map_sequence() -> None:
    inputs = ("A", "B", "C")
    res = map_sequence(inputs)

    unique_new_data = set()
    for _ in res:
        unique_new_data.add(res[_])

    assert len(unique_new_data) == len(res) == len(inputs)

    try:
        map_sequence(("A", "A", "A"))
        assert False
    except Exception as e:
        assert True, e
