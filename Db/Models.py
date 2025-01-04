import os

from peewee import *
from env import BASE_DIR

class LocalMetadata:
    localDBPath = os.path.join(BASE_DIR, "jocelinefb.db")
    localDB = SqliteDatabase(localDBPath)

class Local:
    class Fixture(Model):
        fixture_id = TextField(unique=True)
        fail_count = IntegerField()
        online = BooleanField()

        class Meta:
            database = LocalMetadata.localDB

    class User(Model):
        id = AutoField()
        username = TextField(unique=True)
        password = TextField()

        class Meta:
            database = LocalMetadata.localDB

    class Config(Model):
        configId = IntegerField(unique=True)
        max_fail_count = IntegerField()
        block_pass = TextField()
        externDbPath = TextField()
        language = TextField()

        class Meta:
            database = LocalMetadata.localDB

    LocalMetadata.localDB.connect()
    LocalMetadata.localDB.create_tables([Fixture, User, Config], safe=True)
