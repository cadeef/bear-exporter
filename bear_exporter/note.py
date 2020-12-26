from peewee import AutoField, BlobField, BooleanField, CharField, IntegerField

from bear_exporter.base import AppleTimestampField, BaseModel


class Note(BaseModel):
    archived = IntegerField(column_name="ZARCHIVED", null=True)
    archived_date = AppleTimestampField(column_name="ZARCHIVEDDATE", null=True)
    conflict_uuid = CharField(column_name="ZCONFLICTUNIQUEIDENTIFIER", null=True)
    conflict_uuid_date = AppleTimestampField(
        column_name="ZCONFLICTUNIQUEIDENTIFIERDATE", null=True
    )
    creation_date = AppleTimestampField(column_name="ZCREATIONDATE", null=True)
    encrypted = IntegerField(column_name="ZENCRYPTED", null=True)
    encrypted_data = BlobField(column_name="ZENCRYPTEDDATA", null=True)
    encryption_uuid = CharField(column_name="ZENCRYPTIONUNIQUEIDENTIFIER", null=True)
    folder = IntegerField(column_name="ZFOLDER", index=True, null=True)
    # has_files = IntegerField(column_name='ZHASFILES', null=True)
    has_files = BooleanField(column_name="ZHASFILES", null=True)
    has_images = IntegerField(column_name="ZHASIMAGES", null=True)
    has_source_code = IntegerField(column_name="ZHASSOURCECODE", null=True)
    last_editing_device = CharField(column_name="ZLASTEDITINGDEVICE", null=True)
    locked = IntegerField(column_name="ZLOCKED", null=True)
    locked_date = AppleTimestampField(column_name="ZLOCKEDDATE", null=True)
    modification_date = AppleTimestampField(column_name="ZMODIFICATIONDATE", null=True)
    order = IntegerField(column_name="ZORDER", null=True)
    order_date = AppleTimestampField(column_name="ZORDERDATE", null=True)
    password = IntegerField(column_name="ZPASSWORD", index=True, null=True)
    deleted = IntegerField(column_name="ZPERMANENTLYDELETED", null=True)
    pinned = IntegerField(column_name="ZPINNED", null=True)
    pinned_date = AppleTimestampField(column_name="ZPINNEDDATE", null=True)
    server_data = IntegerField(column_name="ZSERVERDATA", index=True, null=True)
    shown_in_today_widget = IntegerField(column_name="ZSHOWNINTODAYWIDGET", null=True)
    skip_sync = IntegerField(column_name="ZSKIPSYNC", null=True)
    subtitle = CharField(column_name="ZSUBTITLE", null=True)
    text = CharField(column_name="ZTEXT", null=True)
    title = CharField(column_name="ZTITLE", null=True)
    todo_completed = IntegerField(column_name="ZTODOCOMPLETED", null=True)
    todo_in_completed = IntegerField(column_name="ZTODOINCOMPLETED", null=True)
    trashed = BooleanField(column_name="ZTRASHED", null=True)
    trashed_date = AppleTimestampField(column_name="ZTRASHEDDATE", null=True)
    uuid = CharField(column_name="ZUNIQUEIDENTIFIER", null=True)
    vector_clock = BlobField(column_name="ZVECTORCLOCK", null=True)
    z_ent = IntegerField(column_name="Z_ENT", null=True)
    z_opt = IntegerField(column_name="Z_OPT", null=True)
    id = AutoField(column_name="Z_PK", null=True)

    class Meta:
        table_name = "ZSFNOTE"

    def has_includes(self) -> bool:
        """Does note have any included files (or images)?"""
        return self.has_images or self.has_files

    # def files(self) -> List[File]:
    #     """Returns a List of files associated with the note"""
    #     if not self.has_includes():
    #         return []

    #     fc = FileCollection(self.db)
    #     return fc.filter(by="note_id", match=self.id)

    def export(self):
        pass
