from typing import Literal

import core.database.Models as Models
from core import boards, config, fixture

f_data: Models.Local.Fixture
max_fail_count: int

'''
#   Function: load_fixture
#   Desc: Load initial data if it does not exist.
'''
def load_fixture():
    global f_data
    global max_fail_count
    
    try:
        f_data = Models.Local.Fixture().select().where(Models.Local.Fixture.fixture_id == "HR001").get()
    except Models.DoesNotExist:
        f_data = Models.Local.Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
        f_data.save()
        
    max_fail_count = config.getMaxFailCount()
    boards.load_boards_info()


# --- Setters --- #
def set_online(isOnline: bool):
    global f_data

    f_data.online = isOnline
    f_data.save()

def set_fail_count(fail_count):
    global f_data

    f_data.fail_count = fail_count
    f_data.save()

def increment_fixture_fails():
    global f_data

    f_data.fail_count += 1
    f_data.save()

def reset_fail_count():
    set_fail_count(0)


# --- Getters --- #
def is_online(get_status_from_db: bool = False):
    if get_status_from_db:
        try:
            fixture = Models.Local.Fixture().select().where(Models.Local.Fixture.fixture_id == "HR001").get()
        except Models.DoesNotExist:
            fixture = Models.Local.Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
            fixture.save()
            
        return fixture.online
    else:
        global f_data

        return f_data.online
    
def get_fail_count():
    global f_data

    return f_data.fail_count

# functions with extra Logic

def get_fixture_state() -> Literal['Online', 'Offline', 'Blocked']:
    state:Literal['Online', 'Offline', 'Blocked'] = 'Online'

    if not config.get_online_mode() and not is_online():
        state = 'Offline'
        return state
    elif not config.get_online_mode():
        state = 'Offline'
        return state

    state = fixture.check_block_status()
    if state == None:
        return 'Blocked'
    else: 
        return state


