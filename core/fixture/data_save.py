import os
import Db.Models as Models
import core.config as config

from env import BASE_DIR
from .model_manager import is_online

def save_fail(fail_status: int, board_failed: str, iteration_failed: int):
    fail = Models.Local.Fail(
        fail_status = fail_status,
        board_failed = board_failed,
        iteration_failed = iteration_failed
    )
    
    fail.save()
    
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
    
def save_retest_result_in_path(result: str):
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "should_retest") + "", "w") as f:
        f.write(result)

def save_online_result_in_path():
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "fixture_status"), "w") as f:
        f.write(str(is_online()))