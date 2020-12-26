from pathlib import Path
from shutil import copytree
from subprocess import run

import pytest


@pytest.fixture(scope="session")
def bear_data_dir(tmp_path_factory):
    """
    * Sets up test data
    * Returns Path object for data directory
    """
    base = tmp_path_factory.mktemp("bear_data")
    db = base.joinpath("database.sqlite")
    files = base.joinpath("Local Files")

    if not db.is_file():
        create_bear_db(db)

    if not files.is_dir():
        create_bear_files(files)

    return base


def create_bear_files(path: Path):
    copytree(Path("tests/data/bear_files"), path)


def create_bear_db(path: Path):
    run(
        " ".join(["sqlite3", str(path)]),
        input=Path("tests/data/database.sql").read_bytes(),
        check=True,
        capture_output=True,
        shell=True,
    )
