from utils import logger
from utils.logparser import extractFailedPartsInLog

from cli.views import window

from core import boards, config

from udpsocket import client

from core.config import get_online_mode

from .model_manager import *
from .extern_db_manager import *
from .messages import checkFixtureMessages
from .data_save import save_fail, save_test, save_retest_result_in_path
from .status_manager import check_block_status, check_retest_status, set_fixture_online

# --- Core --- #
'''
#   Function: process_info
#   Desc: Main funtion of fixture, this function process all info and events when PCBA was tested in.
#   Arguments:
#       result      | type:str | Test result of PCBA
#       serial      | type:str | PCBA Serial
#       fixture_id  | type:str | FixtureID where PCBA was tested
#       fail_status | type:str | Fail reason code
'''
def process_info(result: str, serial: str, fixture_id: str, fail_status: int):
    # ~ Upper the test result
    result = result.upper()
    
    # ~ If multiboard check_status = False
    check_status = boards.isOnlyOneBoard()
    fixture_messages = checkFixtureMessages()
    
    # ~ Add test log headers
    logger.info(fixture_messages["saving_test"])
    logger.info(f'Serial: {serial}')
    logger.info(f'Result: {result}')
    logger.info(f'FixtureID: {fixture_id}')
    
    # ~ Get the board number by fixture_id
    board_number = fixture_id[-1]
    save_test(serial, result, fail_status, board_number, get_fail_count())
    
    # ~ This because if multiboard all subtest was like one main test.
    if check_status: config.increment_test_count()
    
    if result == "PASS" or result == "PASSED":
        if get_fixture_state() == 'Online':
            remove_serial_parts(serial)
            save_retest_result_in_path("False")
            logger.info(fixture_messages["result_uploaded"])
            set_fixture_online(
                show_unlock_message = False,
                delete_fails = boards.isOnlyOneBoard(),
                modify_fail_count = False
            )
    else:
        # ~ In this part start the fail count if fail_count = 0
        if get_fail_count() == 0: set_fail_count(1)
        # ~ Extract failed devices of PCBA
        partsFailed = extractFailedPartsInLog(fail_status)
        save_fail(fail_status, board_number, get_fail_count())

        # ~ Iterate in all failed devices like a independiente fail.
        i = 1
        for partFailed in partsFailed:
            if get_fixture_state() == 'Online':
                save_part_failed(result, serial, fixture_id, partFailed)
                
                if partFailed == "OTF" or shouldUploadResult(serial, fixture_id, partFailed):
                    save_retest_result_in_path("False")
                    logger.info(fixture_messages["result_uploaded"])
                    boards.setBoardFailed(board_number, True)
                    break
                elif i >= len(partsFailed):
                    save_retest_result_in_path("True")
                    boards.saveBoardShouldRetest(board_number, True)

            else:
                logger.warning(fixture_messages["fixture_locked"])
                break

            i += 1

        # ~ Add test log footer info
        boards.setBoardFailed(board_number, True)
        logger.info(f'Fail Status: {fail_status}')
        logger.info(f'PARTS_FAILED:')
        logger.info(f'{partsFailed}')
        boards.setBoardFailed(board_number, True)
    
    # ~ If multiboard the check_status will be executed in other command (JocelineFB.exe test checkstatus)
    if check_status:
        check_retest_status()
        check_block_status()
    client.send_update_signal()

    # ~ Check the windows array to verify if some window will be executed.
    window.openWindows()
    