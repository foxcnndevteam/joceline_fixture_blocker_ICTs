import sys
from utils import logger, lang

'''
#   Function: getFixtureMessages
#   Desc: Get fixture header object messages.
'''
def getFixtureMessages():
    try:
        return lang.messages["fixture"]
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)


'''
#   Function: checkFixtureMessages
#   Desc: Verify all messages in fixture object.
'''
def checkFixtureMessages():
    und_messages = getFixtureMessages()

    try:
        fixture_messages = {
            'saving_test': und_messages['saving_test'],
            'result_uploaded': und_messages['result_uploaded'],
            'fixture_unlocked': und_messages['fixture_unlocked'],
            'fixture_locked': und_messages['fixture_locked'],
            'max_fail_count_reached': und_messages['max_fail_count_reached'],
            'min_yield_reached': und_messages['min_yield_reached']
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)
        
    return fixture_messages