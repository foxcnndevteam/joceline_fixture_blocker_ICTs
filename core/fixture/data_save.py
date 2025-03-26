import os
from env import BASE_DIR
from core import config
from core.database import Models
from .model_manager import is_online

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
    mode = 'Online' if is_online() else 'Offline'
    
    test = Models.Local.Test(
        serial = serial,
        result = result,
        fail_status = fail_status,
        board_failed = board_failed,
        iteration_failed = iteration_failed,
        test_count = config.get_test_count(),
        mode = mode
    )
    
    test.save()


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
        f.write(str(is_online()))