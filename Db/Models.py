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
        config_id = IntegerField(unique=True)
        max_fail_count = IntegerField()
        block_pass = TextField()
        extern_db_path = TextField()
        language = TextField()
        boards_on_fixture_map = TextField()

        class Meta:
            database = LocalMetadata.localDB
    
    class Boards(Model):
        board_id = IntegerField(unique=True)
        board_failed = BooleanField()
        should_board_retest = BooleanField()
        
        class Meta:
            database = LocalMetadata.localDB
            
    class Fails(Model):
        fail_status = IntegerField()
        board_failed = TextField()
        iteration_failed = IntegerField()
        
        class Meta:
            database = LocalMetadata.localDB
            
    LocalMetadata.localDB.connect()
    LocalMetadata.localDB.create_tables([Fixture, User, Config, Boards, Fails], safe=True)
