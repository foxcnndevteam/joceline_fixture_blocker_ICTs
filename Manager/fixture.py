# File: fixture.py
# Path: Manager/fixture.py

import os
import sys
import logger
import Utils.lang as lang
import Db.Models as Models
import Views.window as window
import Manager.boards as boards
import Manager.config as config

from env import BASE_DIR
from Views.retest import RetestWindow
from Views.blocked import BlockedWindow
from Utils.logparser import extractFailedPartsInLog

f_data: Models.Local.Fixture
max_fail_count: int

def getFixtureMessages():
    try:
        return lang.messages["fixture"]
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)

def loadFixtureInfo():
    global f_data
    global max_fail_count

    try:
        f_data = Models.Local.Fixture().select().where(Models.Local.Fixture.fixture_id == "HR001").get()
    except Models.DoesNotExist:
        f_data = Models.Local.Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
        f_data.save()


    max_fail_count = config.getMaxFailCount()


# --- Setters --- #

def setOnline(isOnline: bool):
    global f_data

    f_data.online = isOnline
    f_data.save()

def setFailCount(fail_count):
    global f_data

    f_data.fail_count = fail_count
    f_data.save()

def incrementFixtureFails():
    global f_data

    f_data.fail_count += 1
    f_data.save()

def resetFailCount():
    setFailCount(0)


# --- Getters --- #

def isOnline():
    global f_data

    return f_data.online
    
def getFailCount():
    global f_data

    return f_data.fail_count


# --- Utils --- #

def saveRetestResultInPath(result: str):
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "should_retest") + "", "w") as f:
        f.write(result)

def saveOnlineResultInPath():
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "fixture_status"), "w") as f:
        f.write(str(isOnline()))

def saveFixtureFail(fail_status: int, board_failed: str, iteration_failed: int):
    fail = Models.Local.Fails(
        fail_status = fail_status,
        board_failed = board_failed,
        iteration_failed = iteration_failed
    )
    
    fail.save()
    
def setFixtureOnline(
        delete_fixture_fails = True, 
        fixture_fail = False, 
        show_unlock_message = True,
        modify_fail_count = True
    ):
    
    fixture_messages = checkFixtureMessages()
    
    setOnline(True)
    
    if delete_fixture_fails: Models.Local.Fails.delete().execute()
    
    if modify_fail_count:
        if fixture_fail: 
            setFailCount(1)
        else:
            resetFailCount()
        
    if show_unlock_message: logger.info(fixture_messages["fixture_unlocked"])


# --- Verifiers --- #

def checkFixtureMessages():
    und_messages = getFixtureMessages()

    try:
        fixture_messages = {
            'saving_test': und_messages['saving_test'],
            'result_uploaded': und_messages['result_uploaded'],
            'fixture_unlocked': und_messages['fixture_unlocked'],
            'fixture_locked': und_messages['fixture_locked'],
            'max_fail_count_reached': und_messages['max_fail_count_reached']
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)
        
    return fixture_messages
    
def shouldCheckFails():
    some_board_failed = boards.someBoardFailed()
    
    if some_board_failed and getFailCount() == 0:
        incrementFixtureFails()
        return False
    elif not some_board_failed:
        setFixtureOnline()
        return False    
    return True

def checkFixtureBlockStatus():
    
    if not shouldCheckFails(): return
    
    fixture_messages = checkFixtureMessages()
    fail_finded = False
    iterations = [[] for _ in range(getFailCount() + 1)]

    for fail in Models.Local.Fails().select(Models.Local.Fails.fail_status, Models.Local.Fails.iteration_failed):
        if not fail.fail_status in iterations[fail.iteration_failed]:
            iterations[fail.iteration_failed].append(fail.fail_status)
            
    for last_fail in iterations[-1]:
        times_finded = 1
        
        for next_iteration in reversed(iterations[0:-1]):
            
            if last_fail in next_iteration:
                times_finded += 1
                fail_finded = True
            else:
                break
            
            if times_finded == config.getMaxFailCount():
                setOnline(False)
                window.show(BlockedWindow('failsLimitReached'))
                logger.warning(fixture_messages["max_fail_count_reached"])
                
    if fail_finded:
        incrementFixtureFails()
    else:
        Models.Local.Fails.delete().where(Models.Local.Fails.iteration_failed != getFailCount()).execute()
        fails = Models.Local.Fails.select()
        for fail in fails:
            fail.iteration_failed = 0
            fail.save()
            
        setFixtureOnline(delete_fixture_fails = False, fixture_fail = True, show_unlock_message = False)
        
def checkFixtureRetestStatus():
    boards_to_retest = boards.getBoardsToRetest()
    if len(boards_to_retest) > 0:
        window.show(RetestWindow(boards_to_retest))
        

# --- Listeners --- #

def onTestSave(result: str, serial: str, fixture_id: str, fail_status: int):
    result = result.upper()
    check_status = boards.isOnlyOneBoard()
    fixture_messages = checkFixtureMessages()
    
    logger.info(fixture_messages["saving_test"])
    logger.info(f'Serial: {serial}')
    logger.info(f'Result: {result}')
    logger.info(f'FixtureID: {fixture_id}')
    
    if result == "PASS" or result == "PASSED":
        if isOnline():
            saveTestInfo(result, serial, fixture_id)
            saveRetestResultInPath("False")
            logger.info(fixture_messages["result_uploaded"])
            setFixtureOnline(
                show_unlock_message = False, 
                delete_fixture_fails = check_status,
                modify_fail_count = False
            )
        elif check_status:
            setFixtureOnline()
            
        return
    else:
        board_number = fixture_id[-1]
        partsFailed = extractFailedPartsInLog(fail_status)
        saveFixtureFail(fail_status, board_number, getFailCount())

        i = 1
        for partFailed in partsFailed:

            if isOnline():
                saveTestInfo(result, serial, fixture_id, partFailed)
                
                if partFailed == "OTF" or shouldUploadResult(serial, fixture_id, partFailed):
                    saveRetestResultInPath("False")
                    logger.info(fixture_messages["result_uploaded"])
                    boards.setBoardFailed(board_number, True)
                    break
                elif i >= len(partsFailed):
                    saveRetestResultInPath("True")
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
        checkFixtureRetestStatus()
        checkFixtureBlockStatus()
    
    window.openWindows()
    

# --- SFC --- #

def saveTestInfo(result, serial, fixture_id, fail_reason = None):
    import Db.Extern as Extern

    if result == "PASS":
        Extern.TestInfo.delete().where(Extern.TestInfo.serial == serial).execute()
    else:
        testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
        testInfo.save()

def shouldUploadResult(serial, fixture_id, fail_reason):
    import Db.Extern as Extern

    fails = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial))
    
    for fail in fails:
        if fixture_id != fail.fixture_id and fail_reason == fail.fail_reason:
            return True

    return False


