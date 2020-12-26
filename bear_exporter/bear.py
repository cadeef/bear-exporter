from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple, Union

import bear_exporter.base as base
from bear_exporter.file import File
from bear_exporter.note import Note
from bear_exporter.tag import Tag, TagIndex


class Bear(object):
    """Interact with Bear"""

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        if base_path:
            self.config = BearConfig(base_path)
        else:
            self.config = BearConfig()

        # Setup the database
        base.database.init(self.config.db_path)

    def tags(self) -> List[Tag]:
        return Tag.select()

    def notes(
        self,
        tag: Optional[Tuple[str]] = None,
        note_id: Optional[Tuple[int]] = None,
        title: Optional[str] = None,
    ) -> List[Note]:
        """Query interface for notes stored in Bear.

        Args:
          tag: str: tag to query (Default value = None)

        Returns:
          A list of Note objects.

        """
        if tag:
            # FIXME: Ugly
            iq1 = Tag.select(Tag.id).where(Tag.title.in_(tag))
            iq2 = TagIndex.select(TagIndex.note).where(TagIndex.tag.in_(iq1))
            result = Note.select().where(Note.id.in_(iq2))
        elif note_id:
            result = Note.select().where(Note.id.in_(note_id))
        elif title:
            result = Note.select().where(Note.title.contains(title))
        else:
            # All not deleted
            result = Note.select().where(Note.trashed == 0)

        return result

    def files(
        self,
        file_id: Optional[Tuple[int]] = None,
        title: Optional[str] = None,
        extension: Optional[str] = None,
    ) -> List[File]:
        """Query interface for files stored in Bear.

        Args:

        Returns:
          A list of File objects.
        """
        if file_id:
            result = File.select().where(File.id.in_(file_id))
        elif title:
            result = File.select().where(File.name.contains(title))
        elif extension:
            result = File.select().where(File.name.endswith(extension))
        else:
            result = File.select()

        return result


class BearException(Exception):
    pass


@dataclass
class BearConfig(object):
    base_path: Union[Path, str] = Path(
        Path.home(),
        "Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data",
    )
    db_file: Path = Path("database.sqlite")
    file_stub: Path = Path("Local Files")

    def __post_init__(self):
        if type(self.base_path) is not Path:
            self.base_path = Path(self.base_path)

    @property
    def db_path(self):
        if not hasattr(self, "_db_path"):
            db = Path(self.base_path, self.db_file)
            # We can't do much of anything without a database
            if not db.is_file():
                raise FileNotFoundError("Database not found: " + str(db))
            self._db_path = db
        return self._db_path

    @property
    def file_path(self):
        return Path(self.base_path, self.file_stub)
