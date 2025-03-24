from core import config
import logger

from cli.views import window
from cli.views.retest import RetestWindow
from cli.views.blocked import BlockedWindow

from Db import Models
from Manager import boards
from .model_manager import get_fail_count, increment_fixture_fails, reset_fail_count, set_fail_count, set_online
from .messages import checkFixtureMessages

def set_fixture_online(
        delete_fails = True, 
        fixture_fail = False, 
        show_unlock_message = True,
        modify_fail_count = True
    ):
    
    fixture_messages = checkFixtureMessages()
    
    set_online(True)
        
    if delete_fails: Models.Local.Fail.delete().execute()
    
    if modify_fail_count:
        if fixture_fail: 
            set_fail_count(1)
        else:
            reset_fail_count()
        
    if show_unlock_message:
        logger.info(fixture_messages["fixture_unlocked"])

def should_check_fails():
    fixture_messages = checkFixtureMessages()
    some_board_failed = boards.someBoardFailed()
    
    if some_board_failed and get_fail_count() == 0:
        increment_fixture_fails()
        return False
    
    elif not some_board_failed:
        if get_fixture_yield() <= config.get_yield_block_threshold():
            set_online(False)
            logger.warning(fixture_messages["min_yield_reached"])
        elif not boards.isOnlyOneBoard():
            set_fixture_online()
        else:
            set_fixture_online(
                show_unlock_message=False
            )
        return False
    return True

def get_fixture_yield():
    sub_query = Models.Local.Test.select(
        Models.Local.Test.test_count
    ).distinct().order_by(
        Models.Local.Test.test_count.desc()
    ).limit(config.gey_yield_calc_qty())

    tests = Models.Local.Test.select(
        Models.Local.Test.id,
        Models.Local.Test.test_count,
        Models.Local.Test.result
    ).where(
        Models.Local.Test.test_count.in_(sub_query)
    ).order_by(Models.Local.Test.test_count.desc())

    test_counts_checked = []
    tests_failed = 0
    test: Models.Local.Test
    
    for test in tests:
        if (not (test.test_count in test_counts_checked)) and (test.result == "FAIL"):
            tests_failed += 1
            test_counts_checked.append(test.test_count)

    yield_calc_qty = config.gey_yield_calc_qty()
    tests_passed = yield_calc_qty - tests_failed
    fixture_yield = (tests_passed / yield_calc_qty) * 100
    
    return int(fixture_yield)

def check_block_status():
    if not should_check_fails(): return
    
    fixture_messages = checkFixtureMessages()
    if get_fixture_yield() <= config.get_yield_block_threshold():
        set_online(False)
        window.show(BlockedWindow('min_yield_reached'))
        logger.warning(fixture_messages["min_yield_reached"])
        return
    
    fail_finded = False
    iterations = [[] for _ in range(get_fail_count() + 1)]

    for fail in Models.Local.Fail().select(Models.Local.Fail.fail_status, Models.Local.Fail.iteration_failed):
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
                set_online(False)
                window.show(BlockedWindow('failsLimitReached'))
                logger.warning(fixture_messages["max_fail_count_reached"])
                
    if fail_finded:
        increment_fixture_fails()
    else:
        Models.Local.Fail.delete().where(Models.Local.Fail.iteration_failed != get_fail_count()).execute()
        fails = Models.Local.Fail.select()
        for fail in fails:
            fail.iteration_failed = 0
            fail.save()
            
        set_fixture_online(delete_fails = False, fixture_fail = True, show_unlock_message = False)
        
def check_retest_status():
    boards_to_retest = boards.getBoardsToRetest()
    if len(boards_to_retest) > 0:
        window.show(RetestWindow(boards_to_retest))