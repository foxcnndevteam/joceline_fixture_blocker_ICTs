import logger

from Utils.logparser import extractFailedPartsInLog

import Manager.boards as boards
import Manager.config as config
import Manager.boards as boards

import cli.views.window as window

from udpsocket import client

from .model_manager import *
from .extern_db_manager import *
from .messages import checkFixtureMessages
from .data_save import save_fail, save_test, save_retest_result_in_path
from .status_manager import check_block_status, check_retest_status, set_fixture_online

# --- Core --- #

def procces_info(result: str, serial: str, fixture_id: str, fail_status: int):
    result = result.upper()
    check_status = boards.isOnlyOneBoard()
    fixture_messages = checkFixtureMessages()
    
    logger.info(fixture_messages["saving_test"])
    logger.info(f'Serial: {serial}')
    logger.info(f'Result: {result}')
    logger.info(f'FixtureID: {fixture_id}')
    
    board_number = fixture_id[-1]
    save_test(serial, result, fail_status, board_number, get_fail_count())
    
    if check_status: config.increment_test_count()
    
    if result == "PASS" or result == "PASSED":
        if is_online():
            remove_serial_parts(serial)
            save_retest_result_in_path("False")
            logger.info(fixture_messages["result_uploaded"])
            set_fixture_online(
                show_unlock_message = False,
                delete_fails = boards.isOnlyOneBoard(),
                modify_fail_count = False
            )
        elif check_status:
            set_fixture_online()
        return
    else:
        if get_fail_count() == 0: set_fail_count(1)
        partsFailed = extractFailedPartsInLog(fail_status)
        save_fail(fail_status, board_number, get_fail_count())

        i = 1
        for partFailed in partsFailed:

            if is_online():
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

        boards.setBoardFailed(board_number, True)
        logger.info(f'Fail Status: {fail_status}')
        logger.info(f'PARTS_FAILED:')
        logger.info(f'{partsFailed}')
        boards.setBoardFailed(board_number, True)
    
    if check_status:
        check_retest_status()
        check_block_status()
        client.send_update_signal()
        
    window.openWindows()
    