import os
from env import BASE_DIR
from peewee import *

dbPath = os.path.join(BASE_DIR, "jocelinefb.db")
db = SqliteDatabase(dbPath)

class Fixture(Model):
    fixture_id = TextField(unique=True)
    fail_count = IntegerField()
    steps_count = IntegerField()
    pass_count= IntegerField()
    online = BooleanField()

    class Meta:
        database = db

class User(Model):
    id = AutoField()
    username = TextField(unique=True)
    password = TextField()

    class Meta:
        database = db

class Config(Model):
    configId = IntegerField(unique=True)
    max_fail_count = IntegerField()
    max_steps_count = IntegerField()
    pctu_steps_lock = IntegerField()
    sfc_path = TextField()

    class Meta:
        database = db

db.connect()
db.create_tables([Fixture, User, Config], safe=True)