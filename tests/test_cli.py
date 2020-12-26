import pytest
from click.testing import CliRunner

import bear_exporter.cli


@pytest.fixture
def cli():
    """
    Returns an instance of click.testing.CliRunner
    """
    return CliRunner()


@pytest.mark.parametrize("item", ["tags", "notes", "files"])
def test_list_items(cli, item):
    result = cli.invoke(eval("bear_exporter.cli.{}".format(item)))
    assert result.exit_code == 0
    assert item.capitalize() in result.output


def test_list_filter(cli):
    pass


@pytest.mark.parametrize("input", ["--", ""])
def test_invalid_args(cli, faker, input):
    """
    Verify bad flags or arguments return an error
    """
    result = cli.invoke(bear_exporter.cli.main, [input + faker.word()])
    assert result.exit_code == 2
