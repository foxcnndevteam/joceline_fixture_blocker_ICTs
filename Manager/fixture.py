import os
import sys
import json
import logger
import peewee
import subprocess
import Utils.lang as lang
import Db.Models as Models
import Manager.config as config

from env import BASE_DIR
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
        f_data = Models.Local.Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
        f_data.save()
    except peewee.IntegrityError:
        f_data = Models.Local.Fixture().select().where(Models.Local.Fixture.fixture_id == "HR001").get()


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

def incrementFixtureFails():
    global f_data

    f_data.fail_count += 1
    f_data.save()

def resetFailCountIfPass(isPass: bool):
    if isPass:
        resetFailCount()

def saveRetestResultInPath(result: str):
    with open(os.path.join(BASE_DIR, "retest_result.txt"), "w") as f:
        f.write(result)

def saveOnlineResultInPath():
    with open(os.path.join(BASE_DIR, "online_result.txt"), "w") as f:
        f.write(str(isOnline()))

def saveBoardNumber(board_number):
    boards_filename = "boards_to_retest.json"
        
    open(os.path.join(BASE_DIR, boards_filename), "a").close()

    with open(os.path.join(BASE_DIR, boards_filename), 'r') as file:
        text = file.read()
        if text == "":
            boards = []
        else:
            boards = json.loads(text)
        boards.append(int(board_number))

    with open(os.path.join(BASE_DIR, boards_filename), "w") as file:
        file.write(str(boards))


# --- Listeners --- #

def onTestSave(result: str, serial: str, fixture_id: str, fail_status: int, not_open_retestview: bool):
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

    logger.info(fixture_messages["saving_test"])
    logger.info(f'Serial: {serial}')
    logger.info(f'Result: {result}')
    logger.info(f'FixtureID: {fixture_id}')
    logger.info(f'Fail Status: {fail_status}')

    board_number = fixture_id[-1]
    partsFailed = extractFailedPartsInLog(fail_status)

    i = 1
    for partFailed in partsFailed:

        if isOnline():
            saveTestInfo(result, serial, partFailed, fixture_id)
            resetFailCountIfPass(result == "PASS" or result == "PASSED")

            if partFailed == "OTF" or ((result == "FAIL" or result == "FAILED") and shouldUploadResult(serial)):
                saveRetestResultInPath("False")
                logger.info(fixture_messages["result_uploaded"])
                break
            elif result == "PASS" or result == "PASSED":
                saveRetestResultInPath("False")
                logger.info(fixture_messages["result_uploaded"])
                break
            elif i >= len(partsFailed):
                saveRetestResultInPath("True")
                if not_open_retestview:
                    saveBoardNumber(board_number)
                else:
                    subprocess.run([str(os.path.join(BASE_DIR, "dist/JocelineFB.exe")), 'window', 'open', 'retestView'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


        else:
            if result == "PASS" or result == "PASSED":
                setOnline(True)
                resetFailCount()
                logger.info(fixture_messages["fixture_unlocked"])
                break
            else:
                logger.warning(fixture_messages["fixture_locked"])
                break

        i += 1

    if result == "FAIL" or result == "FAILED":
        logger.info(f'PARTS_FAILED:')
        logger.info(f'{partsFailed}')

        incrementFixtureFails()

        if isMaxFailsReached():
            setOnline(False)
            subprocess.run([str(os.path.join(BASE_DIR, "JocelineFB.exe")), 'window', 'open', 'blockedView'], capture_output=False)
            logger.warning(fixture_messages["max_fail_count_reached"])


# -- Verifiers --- #

def isMaxFailsReached():
    if getFailCount() >= max_fail_count:
        return True
    return False
    

# --- SFC --- #

def saveTestInfo(result, serial, fail_reason, fixture_id):
    import Db.Extern as Extern

    if result == "PASS":
        Extern.TestInfo.delete().where(Extern.TestInfo.serial == serial).execute()
    else:
        testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
        testInfo.save()

def shouldUploadResult(serial):
    import Db.Extern as Extern

    fails = list(Extern.TestInfo.select().where(Extern.TestInfo.serial == serial))

    for fail in fails:
        for fail2nd in fails:
            if fail.fixture_id != fail2nd.fixture_id and fail.fail_reason == fail2nd.fail_reason:
                return True

    return False