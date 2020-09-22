from pathlib import Path
from typing import List, Optional

import records

DEFAULT_DATA_PATH = Path(
    Path.home(),
    "Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data",
)


class DbObject(object):
    """
    Parent object for database derived objects

    Exports all selected columns as attributes
    """

    def __init__(self, data: records.Record):
        # ... could support other modes but lazy wins
        if not isinstance(data, records.Record):
            raise TypeError(
                "Not sure how to handle anything other than records.Record..."
            )

        self.__db_record = data

    def __getattr__(self, key) -> str:
        # Fix Bear's nutty column naming scheme
        key = "Z{}".format(key).upper()

        try:
            return self.__db_record[key]
        except KeyError as e:
            raise AttributeError(e)

    @property
    def key(self):
        return self._pk


class File(DbObject):
    """
    File object
    """

    @property
    def path(self) -> Path:
        # I have no idea why Bear differntiates the storage path between images and other
        # files, but we'll deal with it crudely
        if self.is_image():
            modifier = "Note Images"
        else:
            modifier = "Note Files"

        return Path(modifier, self.uniqueidentifier, self.filename)

    def is_image(self) -> bool:
        return self.normalizedfileextension in ("png", "jpeg", "gif")


class Note(DbObject):
    """
    Note object
    """

    def title_slug(self, length: int = 128) -> str:
        # TODO: parse title_slug from title
        return "hi"

    def has_files(self) -> bool:
        return bool(self.hasfiles)

    def has_images(self) -> bool:
        return bool(self.hasimages)

    def files(self) -> List[File]:
        if not (self.has_images() or self.has_files()):
            return []

        # FIXME: Use passed path rather than default
        db: records.Database = Bear().db()
        query = """
            select *
            from ZSFNOTEFILE
            where ZNOTE = :noteid
        """
        return list(map(File, db.query(query, noteid=self._pk)))


class Bear(object):
    """
    Interact with Bear
    """

    def __init__(self, base_path: Optional[str] = None) -> None:
        self._base_path: Path = Path(base_path or DEFAULT_DATA_PATH)
        self._db_file: Path = self._base_path.joinpath("database.sqlite")
        self._file_path: Path = self._base_path.joinpath("Local Files")

        # We can't do much of anything without a database
        if not self._db_file.is_file():
            raise FileNotFoundError("Database not found: {}".format(self._db_file))

    def db(self) -> records.Database:
        if not hasattr(self, "_db"):
            self._db: records.Database = records.Database(
                "sqlite:///{}".format(self._db_file)
            )
        return self._db

    def tags(self) -> List[str]:
        query = """
            select ZTITLE
            from ZSFNOTETAG
        """
        return list(map(lambda r: r.get("ZTITLE"), self.db().query(query)))

    def notes(self) -> List[Note]:
        """
        Returns a list of Note objects

        TODO: Add filtering
        FIXME: probably should limit
        """
        query = """
            select *
            from ZSFNOTE
        """
        return list(map(Note, self.db().query(query)))

    def files(self) -> List[File]:
        """
        Returns a list of files
        """
        query = """
            select *
            from ZSFNOTEFILE
        """
        return list(map(File, self.db().query(query)))
