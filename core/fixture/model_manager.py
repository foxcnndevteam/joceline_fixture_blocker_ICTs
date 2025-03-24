import core.database.Models as Models
from core import boards, config

f_data: Models.Local.Fixture
max_fail_count: int

def load_fixture_info():
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

def is_online():
    global f_data

    return f_data.online
    
def get_fail_count():
    global f_data

    return f_data.fail_count