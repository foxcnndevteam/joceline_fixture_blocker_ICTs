import logging
from core.database import Models
from peewee import DataError, DatabaseError, InternalError, OperationalError
from core.api import SFC_check_ICT_Repair
from core.config import get_force_3t, get_ask_fail_mode, get_parts
from utils import logger
from .log_retest_manager import FailLogFile
import json
from utils.logparser import is_mac_fru_valid
from cli.views import window
from cli.views.blocked import BlockedWindow
from env import today

'''
#   Function: remove_serial_parts
#   Desc: Remove all failed devices by PCBA serial saved in extern database 
#   Arguments:
#       serial | type:str | PCBA Serial
''' 
def remove_serial_parts(serial: str):
    try:
        from core.database import Extern
        Extern.TestInfo.delete().where(Extern.TestInfo.serial == serial).execute()
        logging.info(f"External DB: deleted fails with serial: {serial}")
    except DatabaseError:
        logging.info(f"DatabaseError: Error when delete with {serial}")
    except DataError:
        logging.info(f"DataError: Error when delete with {serial}")
    except InternalError:
        logging.info(f"InternalError: Error when delete with {serial}")
    except OperationalError:
        logging.info(f"OperationalError: Error when delete with {serial}")


'''
#   Function: save_part_failed
#   Desc: Save a failed device of PCBA
#   Arguments:
#       result      | type:str | Test result of PCBA
#       serial      | type:str | PCBA Serial
#       fixture_id  | type:str | FixtureID where PCBA was tested
#       fail_reason | type:str | Fail reason code
'''
def save_test_result_ext(result: str, serial: str, fixture_id: str, fail_reason: str = None, fail_reason_json: list[str] = []):
    tries = 0
    retest_file = FailLogFile(serial)
    if result == 'FAIL':
        retest_file.add_fail(fail_reason_json)
    else:
        retest_file.remove_file()

    while (tries < 4):
        try:
            from core.database import Extern
            testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id, result = result, date=today)
            testInfo.save()
            logging.info(f"External DB: test info added with serial:{serial} fixture_id:{fixture_id} fail_reason:{fail_reason} result: {result}")
            break
        except DatabaseError:
            logging.info(f"DatabaseError: Error when adding with {serial}")
            tries += 1
        except DataError:
            logging.info(f"DataError: Error when adding with {serial}")
            tries += 1
        except InternalError:
            logging.info(f"InternalError: Error when adding with {serial}")
            tries += 1
        except OperationalError:
            logging.info(f"OperationalError: Error when adding with {serial}")
            tries += 1
        except TimeoutError:
            logging.info(f"Timeout Error: Error when adding with {serial}")
            tries += 1


def same_fails(test1: str, test2: str) -> bool:
    coincidences = 0

    test1_json = json.loads(test1.replace("'", '"'))
    test2_json = json.loads(test2.replace("'", '"'))

    test1_obj = {}
    for test in test1_json:
        test1_obj[test] = test

    for test2 in test2_json:
        if test1_obj.get(test2):
            coincidences += 1

    return coincidences > 0

'''
#   Function: shouldUploadResult
#   Desc: Check if PCBA serial whould be failed or retested
#   Arguments:
#       result      | type:str | Test result of PCBA
#       fixture_id  | type:str | FixtureID where PCBA was tested
#       fail_reason | type:str | Fail reason code
'''
def shouldUploadResult(serial, fixture_id, r_ict_count: int = None):
    from core.database import Extern

    try:
        ict_repair_count = 0
        if r_ict_count == None:
            ict_repair_count = SFC_check_ICT_Repair(serial)
        else:
            ict_repair_count = r_ict_count
        # threshold = get_max_tries()

        fails_found = 0
        repair_info_list = list(Extern.RepairInfo.select(Extern.RepairInfo.date).where(Extern.RepairInfo.serial == serial).limit(1).order_by(Extern.RepairInfo.date.desc()))

        if len(repair_info_list) != 0:
            date_filter = repair_info_list[0].date
            fails_list = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial, Extern.TestInfo.result == 'FAIL', Extern.TestInfo.date > date_filter))
        else:
            fails_list = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial, Extern.TestInfo.result == 'FAIL'))
        fails_found = len(fails_list)

        if fails_found < 2:
            return False
        
        if fails_found == 2:
            fail_reason1 = fails_list[0].fail_reason
            fail_reason2 = fails_list[1].fail_reason
            if same_fails(fail_reason1, fail_reason2):
                Extern.RepairInfo(serial=serial, date=today).save()
                return True
            else:
                return False

        logging.info(f"External DB:{fails_found} fails found with serial {serial} ")
        should_uplaod = fails_found >= 3
        if should_uplaod:
            Extern.RepairInfo(serial=serial, date=today).save()
        return  should_uplaod
    except DatabaseError:
        logging.info(f"DatabaseError: Error when consulting with {serial}")
    except DataError:
        logging.info(f"DataError: Error when consulting with {serial}")
    except InternalError:
        logging.info(f"InternalError: Error when consulting with {serial}")
    except OperationalError:
        logging.info(f"OperationalError: Error when consulting with {serial}")

    return False

class BoolContainer:
    fail: bool
    def __init__(self):
        self.fail = True

    def set_val(self, new_val:bool):
        self.fail = new_val

def eval_show_auth_window() -> bool:
    current_config = get_ask_fail_mode()
    
    if current_config in ["partial", "full"]:
        return True

    return False

def should_show_window(parts_failed: list[str] = []) -> bool:
    current_config = get_ask_fail_mode()

    if current_config == "full" and len(parts_failed) > 0:
        return True

    if current_config == "partial" and len(parts_failed) > 0:
        parts_list = get_parts().split(",")
        
        for part_failed in parts_failed:
            for part in parts_list:
                if part in part_failed:
                    return True

    return False

def allow_retest(serial:str, failed_parts = [], result = "PASS"):

    if eval_show_auth_window() and should_show_window(failed_parts) and result != "PASS":
        fcontainer = BoolContainer()
        window.openWindowAuth(fcontainer.set_val, f"failed parts: {failed_parts}")
        return not fcontainer.fail

    log_file = FailLogFile(serial)

    retest = log_file.allow_retest()

    if not retest:
        from core.database import Extern
        Extern.RepairInfo(serial=serial, date=today).save()
        log_file.remove_file()

    fru_mac_correct_result = is_mac_fru_valid(serial)

    if not fru_mac_correct_result["result"] and fru_mac_correct_result["found"]:
        logger.info(f"FRU and/or MAC incorrect")
        window.show(BlockedWindow("wrong_fru_mac"))
        return True

    return retest
