import os
import sys
from peewee import *
from core import config
from utils import logger
import datetime

'''
#   Class: ExternMetadata
#   Desc: Save static data used in extern database
'''
class ExternMetadata:
    # ~ Get the extern database path
    extern_db_path = config.getExternDbPath()
    
    # ~ If Extern db path not exist, get error.
    if not os.path.isdir(os.path.dirname(extern_db_path)):
        logger.error('Missing \'Extern db\' file')
        sys.exit(0)
        
    globalDB = SqliteDatabase(extern_db_path, timeout=1, check_same_thread=False)


'''
#   Class: TestInfo
#   Desc: This database model is used to save all tests in one database, used to check all fixture tests fails in PCB retest.
'''
class TestInfo(Model):
    id = AutoField()
    serial = TextField(index=True)
    fail_reason = TextField()
    result = TextField(index=True)
    fixture_id = TextField()
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = ExternMetadata.globalDB

class RepairInfo(Model):
    id = AutoField()
    serial = TextField(index=True)
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = ExternMetadata.globalDB

ExternMetadata.globalDB.connect()
ExternMetadata.globalDB.create_tables([TestInfo, RepairInfo], safe=True)