from data_transformations.citibike import ingest


def test_should_sanitize_nothing() -> None:
    no_whitespace_columns = ["foo"]

    actual = ingest.sanitize_columns(no_whitespace_columns)
    expected = no_whitespace_columns

    assert expected == actual


def test_should_sanitize_whitespace_outside() -> None:
    no_whitespace_columns = [" foo "]

    actual = ingest.sanitize_columns(no_whitespace_columns)
    expected = ["foo"]

    assert expected == actual


def test_should_sanitize_whitespace_in_between() -> None:
    no_whitespace_columns = ["foo bar"]

    actual = ingest.sanitize_columns(no_whitespace_columns)
    expected = ["foo_bar"]

    assert expected == actual

def test_sanitize_columns():
    cols = ["start station id", "end station name", "start station_latitude"]
    assert ingest.sanitize_columns(cols) == ["start_station_id", "end_station_name", "start_station_latitude"]
