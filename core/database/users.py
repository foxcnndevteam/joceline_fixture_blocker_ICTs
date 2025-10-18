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
#   Class: Users
#   Desc: Database of users who can authorize or deny the tests.
'''
class Users(Model):
    id = AutoField()
    emp_number = TextField(index=True)
    password = TextField()

    class Meta:
        database = ExternMetadata.globalDB


ExternMetadata.globalDB.connect()
ExternMetadata.globalDB.create_tables([Users], safe=True)