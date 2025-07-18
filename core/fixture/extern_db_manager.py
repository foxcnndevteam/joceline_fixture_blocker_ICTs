import logging
from peewee import DataError, DatabaseError, InternalError, OperationalError
from core.api import SFC_check_ICT_Repair

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
def save_part_failed(result: str, serial: str, fixture_id: str, fail_reason: str = None):
    tries = 0
    while (tries < 4):
        try:
            from core.database import Extern
            testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
            testInfo.save()
            logging.info(f"External DB: fail added with serial:{serial} fixture_id:{fixture_id} fail_reason:{fail_reason}")
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


'''
#   Function: shouldUploadResult
#   Desc: Check if PCBA serial whould be failed or retested
#   Arguments:
#       result      | type:str | Test result of PCBA
#       fixture_id  | type:str | FixtureID where PCBA was tested
#       fail_reason | type:str | Fail reason code
'''
def shouldUploadResult(serial, fixture_id, fail_reason):
    from core.database import Extern

    try:
        ict_repair_count = SFC_check_ICT_Repair(serial)

        threshold = 2 * (1 + ict_repair_count)

        fails = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial))
    
        fails_found = len(fails)

        logging.info(f"External DB:{fails_found} fails found with serial {serial} ")
        should_uplaod = len(fails) > threshold
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