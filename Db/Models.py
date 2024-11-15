import os
import json
from env import BASE_DIR
from peewee import *

localDBPath = os.path.join(BASE_DIR, "jocelinefb.db")
localDB = SqliteDatabase(localDBPath)

class Fixture(Model):
    fixture_id = TextField(unique=True)
    fail_count = IntegerField()
    steps_count = IntegerField()
    pass_count= IntegerField()
    online = BooleanField()

    class Meta:
        database = localDB

class User(Model):
    id = AutoField()
    username = TextField(unique=True)
    password = TextField()

    class Meta:
        database = localDB

class Config(Model):
    configId = IntegerField(unique=True)
    max_fail_count = IntegerField()
    max_steps_count = IntegerField()
    pctu_steps_lock = IntegerField()
    sfc_path = TextField()
    binaryPath = TextField()
    apiUrl = TextField()
    sfc_mode = IntegerField()

    class Meta:
        database = localDB

localDB.connect()
localDB.create_tables([Fixture, User, Config], safe=True)

# ---------------------------- Extern DB ---------------------------- #

confFileName = "jocelinefb.conf.json"

with open(os.path.join(BASE_DIR, confFileName), 'r') as file:
    confFile = json.loads(file.read())
globalDBPath = confFile["externDBPath"]

globalDB = SqliteDatabase(globalDBPath)

class TestInfo(Model):
    id = AutoField()
    serial = TextField()
    fail_reason = TextField()
    fixture_id = TextField()

    class Meta:
        database = globalDB

globalDB.connect()
globalDB.create_tables([TestInfo], safe=True)