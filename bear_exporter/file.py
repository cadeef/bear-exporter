from pathlib import Path

from peewee import AutoField, BooleanField, CharField, IntegerField

from bear_exporter.base import AppleTimestampField, BaseModel


class File(BaseModel):
    # animated = IntegerField(column_name='ZANIMATED', null=True)
    animated = BooleanField(column_name="ZANIMATED", null=True)
    creation_date = AppleTimestampField(column_name="ZCREATIONDATE", null=True)
    downloaded = IntegerField(column_name="ZDOWNLOADED", null=True)
    duration = IntegerField(column_name="ZDURATION", null=True)
    name = CharField(column_name="ZFILENAME", null=True)
    size = IntegerField(column_name="ZFILESIZE", null=True)
    height = IntegerField(column_name="ZHEIGHT", null=True)
    height1 = IntegerField(column_name="ZHEIGHT1", null=True)
    index = IntegerField(column_name="ZINDEX", null=True)
    last_editing_device = CharField(column_name="ZLASTEDITINGDEVICE", null=True)
    modification_date = AppleTimestampField(column_name="ZMODIFICATIONDATE", null=True)
    normalized_file_extension = CharField(
        column_name="ZNORMALIZEDFILEEXTENSION", null=True
    )
    note = IntegerField(column_name="ZNOTE", index=True, null=True)
    # deleted = IntegerField(column_name='ZPERMANENTLYDELETED', null=True)
    deleted = BooleanField(column_name="ZPERMANENTLYDELETED", null=True)
    server_data = IntegerField(column_name="ZSERVERDATA", index=True, null=True)
    skip_sync = IntegerField(column_name="ZSKIPSYNC", null=True)
    uuid = CharField(column_name="ZUNIQUEIDENTIFIER", null=True)
    unused = IntegerField(column_name="ZUNUSED", null=True)
    uploaded = IntegerField(column_name="ZUPLOADED", null=True)
    uploaded_date = AppleTimestampField(column_name="ZUPLOADEDDATE", null=True)
    width = IntegerField(column_name="ZWIDTH", null=True)
    width1 = IntegerField(column_name="ZWIDTH1", null=True)
    z_ent = IntegerField(column_name="Z_ENT", index=True, null=True)
    z_opt = IntegerField(column_name="Z_OPT", null=True)
    id = AutoField(column_name="Z_PK", null=True)

    class Meta:
        table_name = "ZSFNOTEFILE"

    @property
    def path(self) -> Path:
        """ """
        # I have no idea why Bear differntiates the storage path between images and other
        # files, but we'll deal with it crudely
        if self.is_image():
            modifier = "Note Images"
        else:
            modifier = "Note Files"

        return Path(modifier, self.uuid, self.name)

    def is_image(self) -> bool:
        """ """
        return self.normalized_file_extension in ("png", "jpeg", "gif")
