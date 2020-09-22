import pytest

from bear_exporter.bear import Bear


@pytest.fixture
def bear(base_data_dir):
    """
    Returns a primed instance of the Bear object for testing
    """
    return Bear(base_path=base_data_dir)


@pytest.mark.parametrize("item, length", [("tags", 6), ("notes", 4), ("files", 4)])
def test_item_all(bear, item, length):
    """
    Rudimentary check to ensure a list of all items returns the expected number of records
    """
    result = eval("bear.{}()".format(item))
    assert len(result) == length
