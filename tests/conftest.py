import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def base_data_dir(shared_datadir):
    """
    * Uses shared_datadir fixture
    * Sets up test data
    * Returns Path object for data directory
    """
    if create_test_db(shared_datadir):
        return shared_datadir


def create_test_db(path: Path):
    # FIXME: Handle DB import properly
    subprocess.run(
        ["sqlite3", str(path.joinpath("database.sqlite"))],
        input=path.joinpath("database.sql").read_bytes(),
        check=True,
    )
    return True
