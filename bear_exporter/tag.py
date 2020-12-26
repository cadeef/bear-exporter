from peewee import AutoField, CharField, CompositeKey, IntegerField

from bear_exporter.base import AppleTimestampField, BaseModel


class Tag(BaseModel):
    modification_date = AppleTimestampField(column_name="ZMODIFICATIONDATE", null=True)
    title = CharField(column_name="ZTITLE", null=True)
    z_ent = IntegerField(column_name="Z_ENT", null=True)
    z_opt = IntegerField(column_name="Z_OPT", null=True)
    id = AutoField(column_name="Z_PK", null=True)

    class Meta:
        table_name = "ZSFNOTETAG"


class TagIndex(BaseModel):
    tag = IntegerField(column_name="Z_14TAGS", null=True)
    note = IntegerField(column_name="Z_7NOTES", null=True)

    class Meta:
        table_name = "Z_7TAGS"
        indexes = (
            (("z_14_tags", "z_7_notes"), False),
            (("z_7_notes", "z_14_tags"), True),
        )
        primary_key = CompositeKey("z_14_tags", "z_7_notes")
