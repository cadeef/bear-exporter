from datetime import datetime
from typing import Union

from peewee import Field, Model, SqliteDatabase

database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class AppleTimestampField(Field):
    field_type = "text"

    def db_value(self, value) -> None:
        # YOLO: We aren't writing back, this'll be a neat bug later
        pass

    def python_value(self, value) -> Union[datetime, None]:
        # Apple Core Data timestapms begin at January 1, 2001 (+31 years) rather than normal epoch
        if value:
            return datetime.fromtimestamp(value + 978307200)
        else:
            return None
