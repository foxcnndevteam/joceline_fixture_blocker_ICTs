from typing import Literal
from utils import logger

from cli.views import window
from cli.views.retest import RetestWindow
from cli.views.blocked import BlockedWindow

from core.database import Models
from core import boards, config

from .model_manager import get_fail_count, increment_fixture_fails, reset_fail_count, set_fail_count, set_online
from .messages import checkFixtureMessages

'''
#   Function: set_fixture_online
#   Desc: Main funtion of fixture, this function process all info and events when PCBA was tested in.
#   Arguments:
#       delete_fails        | type:bool | Indicates if should delete fails when online.
#       fixture_fail        | type:bool | Indicates if fixture fail.
#       show_unlock_message | type:bool | Indicates if show unlock message when pass.
#       modify_fail_count   | type:bool | Indicates of should modify fail count (Used in multiboard).
'''
def set_fixture_online(
        delete_fails: bool = True, 
        fixture_fail: bool = False, 
        show_unlock_message: bool = True,
        modify_fail_count: bool = True
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


'''
#   Function: should_check_fails
#   Desc: Checks if fixture fail or yield is not above the threshold to indicate if should be check fails.
'''
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


'''
#   Function: get_fixture_yield 
#   Desc: Calculates the fixture yield in single board or multiboard tests.
'''
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


'''
#   Function: check_block_status 
#   Desc: If should check fails and yield is above threshold this function checks 
#         fails saved in Fail model to determinate if fixture should be blocked, 
#         the function check the fail an iteration to verify if has a consecutive 
#         fail, that because if use multiboard the fixture save 2 or more fails
#         in database labeled with some iteration number, the iteration indicates 
#         the main test itertaion number in fail because in multiboard the process_info
#         function is executed multiple times and it save multiple subtests, the fixture 
#         create an iteration (Like main fail id) to check where the fail was happen.
'''
def check_block_status() -> Literal['Online', 'Offline', 'Blocked', None]:
    if not should_check_fails(): return 'Online'
    
    fixture_messages = checkFixtureMessages()
    if get_fixture_yield() <= config.get_yield_block_threshold():
        set_online(False)
        window.show(BlockedWindow('min_yield_reached'))
        logger.warning(fixture_messages["min_yield_reached"])
        return 'Blocked'
    
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
                return 'Blocked'
                
    if fail_finded:
        increment_fixture_fails()
        return 'Online'
    else:
        Models.Local.Fail.delete().where(Models.Local.Fail.iteration_failed != get_fail_count()).execute()
        fails = Models.Local.Fail.select()
        for fail in fails:
            fail.iteration_failed = 0
            fail.save()
            
        set_fixture_online(delete_fails = False, fixture_fail = True, show_unlock_message = False)
        return 'Online'

'''
#   Function: check_retest_status 
#   Desc: Checks if some board should be retested to display retest window.
'''  
def check_retest_status():
    boards_to_retest = boards.getBoardsToRetest()
    if len(boards_to_retest) > 0:
        window.show(RetestWindow(boards_to_retest))