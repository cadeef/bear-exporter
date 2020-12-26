import pytest

from bear_exporter.bear import Bear


@pytest.fixture
def bear(bear_data_dir):
    """
    Returns a primed instance of the Bear object for testing
    """
    return Bear(base_path=bear_data_dir)


@pytest.mark.parametrize("item, length", [("tags", 6), ("notes", 4), ("files", 4)])
def test_item_all(bear, item, length):
    """
    Rudimentary check to ensure a list of all items returns the expected number of records
    """
    result = getattr(bear, item)()
    assert len(result) == length


# @pytest.mark.parametrize("tag, length", [("welcome", 4), ("supernonexistent", 0)])
# def test_note_filter_by_tag(bear, tag, length):
#     # result = bear.notes(tag=tag).dicts()
#     result = bear.notes()

#     for r in result:
#         print(result)

#     assert 0
#     assert len(result) == length
