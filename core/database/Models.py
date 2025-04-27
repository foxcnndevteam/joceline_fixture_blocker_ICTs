import os
import datetime
from peewee import *
from env import BASE_DIR

'''
#   Class: LocalMetadata
#   Desc: Save static data used in local database
'''
class LocalMetadata:
    # ~ The local database is alway located at ./ of the software path
    localDBPath = os.path.join(BASE_DIR, "jocelinefb.db")
    localDB = SqliteDatabase(localDBPath)


'''
#   Class: Local
#   Desc: Save all local models
'''
class Local:
    
    '''
    #   Class: Fixture
    #   Desc: Table to save fixture info
    '''
    class Fixture(Model):
        fixture_id = TextField(unique=True)
        fail_count = IntegerField()
        online = BooleanField()

        class Meta:
            database = LocalMetadata.localDB


    '''
    #   Class: User
    #   Desc: Table to save user credentials
    '''
    class User(Model):
        id = AutoField()
        username = TextField(unique=True)
        password = TextField()

        class Meta:
            database = LocalMetadata.localDB


    '''
    #   Class: Config
    #   Desc: Table to save config info
    '''
    class Config(Model):
        config_id = IntegerField(unique=True)
        max_fail_count = IntegerField()
        block_pass = TextField()
        extern_db_path = TextField()
        server_log_path = TextField()
        language = TextField()
        boards_on_fixture_map = TextField()
        yield_calc_quantity = IntegerField(
            default=10
        )
        yield_block_threshold = IntegerField(
            default=60
        )
        test_count = IntegerField( default=0 )
        udp_server_port = IntegerField()
        pause_on_fail = BooleanField()
        online_mode = BooleanField()

        class Meta:
            database = LocalMetadata.localDB


    '''
    #   Class: Board
    #   Desc: Table to save boards info if multiple boards
    '''    
    class Board(Model):
        board_id = IntegerField(unique=True)
        board_failed = BooleanField()
        should_board_retest = BooleanField()
        
        class Meta:
            database = LocalMetadata.localDB
    
    
    '''
    #   Class: Test
    #   Desc: Table to save test info. This table save all the tests in fixture an this is the difference between Test and Fail
    '''
    class Test(Model):
        serial = TextField()
        result = TextField()
        fail_status = IntegerField()
        board_failed = TextField()
        date = DateTimeField(default=datetime.datetime.now)
        test_count = IntegerField()
        mode = TextField()

        class Meta:
            database = LocalMetadata.localDB


    '''
    #   Class: Fail
    #   Desc: Table to save fail info. This table is cleaned when fixture test pass
    '''
    class Fail(Model):
        fail_status = IntegerField()
        board_failed = TextField()
        iteration_failed = IntegerField()
        
        class Meta:
            database = LocalMetadata.localDB
            
    LocalMetadata.localDB.connect()
    LocalMetadata.localDB.create_tables([Fixture, User, Config, Board, Test, Fail], safe=True)
