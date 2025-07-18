import os
from env import BASE_DIR
from core import config
from core.api import SFC_check_ICT_Repair
from core.database import Models
from .model_manager import is_online
from .model_manager import get_fixture_state
from core.config import get_online_mode
from env import today
import datetime 

'''
#   Function: save_fail
#   Desc: Save fail info in local database
#   Arguments:
#       fail_status         | type:int | Fail status code
#       board_failed        | type:str | The board where PCB failed
#       iteration_failed    | type:int | The iteration in fail count
'''
def save_fail(fail_status: int, board_failed: str, iteration_failed: int):
    
    # ~ When the fixture fail it start to acumulate fails, if the second time the 
    # fix fail it will add 1 to iteration, same the three, four, etc. When the fixture 
    # pass or all the boards pass it will return to 0It to check in which fail the 
    # status code fail this only works in multi board, in single board mode it always is 0.
    
    fail = Models.Local.Fail(
        fail_status = fail_status,
        board_failed = board_failed,
        iteration_failed = iteration_failed
    )
    
    fail.save()


def save_failed_parts(fixture_id: str, parts_failed: list[str]):
    parts_failed_str = ''

    for part in parts_failed:
        if parts_failed_str != '':
            parts_failed_str += ','
        parts_failed_str += part

    part_f = Models.Local.FailsHistory(
        fixture_id = fixture_id,
        fails = parts_failed_str
    )

    part_f.save()

'''
#   Function: save_test
#   Desc: Save test info in local database
#   Arguments:
#       serial              | type:str | PCBA Serial
#       result              | type:str | Result of the test
#       fail_status         | type:int | Fail status code
#       board_failed        | type:str | The board where PCB failed
#       iteration_failed    | type:int | The iteration in fail count
'''   
def save_test(serial: str, result: str, fail_status: int, board_failed: str, iteration_failed: int):
    mode = get_fixture_state(False)
    
    test = Models.Local.Test(
        serial = serial,
        result = result,
        fail_status = fail_status,
        board_failed = board_failed,
        iteration_failed = iteration_failed,
        test_count = config.get_test_count(),
        mode = mode,
        date = today
    )
    
    test.save()

def should_retest_in_station(serial: str, ICT_repair_count: int = 0):
    threshold = 3

    if ICT_repair_count == 1:
        threshold = 4
    elif ICT_repair_count == 2:
        threshold = 6
    elif ICT_repair_count >= 3:
        threshold = 8

    tests = Models.Local.Test.select(Models.Local.Test.id).where(Models.Local.Test.serial).where(Models.Local.Test.serial.__eq__(serial),
        Models.Local.Test.result.startswith('FAIL')).execute()

    tests_count = len(tests)
    
    return tests_count < threshold


def save_allow_retest_query(serial: str, boardnumber: int) -> bool:
    #tests = Models.Local.Test.select(
    #    Models.Local.Test.serial).where(Models.Local.Test.serial.__eq__(serial),
    #    Models.Local.Test.result.startswith('FAIL'),
    #    Models.Local.Test.board_failed.__eq__(int(boardnumber))
    #).execute()
    tests = Models.Local.Test().select(
            Models.Local.Test.id,
            Models.Local.Test.serial,
            Models.Local.Test.result,
            Models.Local.Test.fail_status,
            Models.Local.Test.board_failed,
            Models.Local.Test.date,
            Models.Local.Test.mode
        ).limit(2).order_by(
            Models.Local.Test.date.desc()
        )
    if len(tests) < 2:
        return False

    should_retest = should_retest_in_station(serial)

    return tests[1].serial == serial and should_retest

def save_allow_test_query(serial: str) -> bool:
    # ICT_Reapir_count = SFC_check_ICT_Repair(serial)

    # threshold = 2

    # if ICT_Reapir_count == 1:
    #     threshold = threshold * 2
    # elif ICT_Reapir_count == 2:
    #     threshold = threshold * 3
    # elif ICT_Reapir_count >= 3:
    #     threshold = threshold * 4

    # tests = Models.Local.Test.select(
    #     Models.Local.Test.serial).where(Models.Local.Test.serial.__eq__(serial),
    #     Models.Local.Test.result.startswith('FAIL')
    # ).execute()

    # allow_test = len(tests) < threshold

    tests = list(Models.Local.Test.select(Models.Local.Test.serial, Models.Local.Test.result).limit(1).order_by(Models.Local.Test.date.desc()).execute())

    if len(tests) == 0:
        return True

    allow_test = not tests[0].serial == serial or tests[0].result == 'PASS'

    return allow_test

'''
#   Function: save_retest_result_in_path
#   Desc: Save if the PCBA should be retested in an output file to be readed by testplan.
#   Arguments:
#       result              | type:str | Result of the test
'''   
def save_retest_result_in_path(result: str):
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "should_retest") + "", "w") as f:
        f.write(result)


'''
#   Function: save_online_result_in_path
#   Desc: Save if the fixture status is online in an output file to be readed by testplan.
'''
def save_online_result_in_path():
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "fixture_status"), "w") as f:
        f.write(str(is_online() and config.get_online_mode()))

'''
#   Function: save_should_pause_in_path
#   Desc: Save if should pause on fail in an output file to be readed by testplan.
'''
def save_should_pause_in_path():
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)

    with open(os.path.join(result_path, "should_pause"), "w") as f:
        f.write(str(config.get_pause_on_fail()))

'''
#   Function: allow_test_in_path
#   Desc: Save if should allow the test if the biard in an output file to be readed by testplan.
'''

def save_allow_test_in_path(allow_test: bool):
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)

    with open(os.path.join(result_path, "allow_test"), "w") as f:
        f.write(str(allow_test))
