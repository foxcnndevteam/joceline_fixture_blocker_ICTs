import os
import sys
from peewee import *
from core import config
from utils import logger

class ExternMetadata:
    extern_db_path = config.getExternDbPath()
    if not os.path.isdir(os.path.dirname(extern_db_path)):
        logger.error('Missing \'Extern db\' file')
        sys.exit(0)
    globalDB = SqliteDatabase(extern_db_path)

class TestInfo(Model):
    id = AutoField()
    serial = TextField()
    fail_reason = TextField()
    fixture_id = TextField()

    class Meta:
        database = ExternMetadata.globalDB

ExternMetadata.globalDB.connect()
ExternMetadata.globalDB.create_tables([TestInfo], safe=True)