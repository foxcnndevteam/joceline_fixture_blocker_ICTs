'''
#   Function: remove_serial_parts
#   Desc: Remove all failed devices by PCBA serial saved in extern database 
#   Arguments:
#       serial | type:str | PCBA Serial
''' 
def remove_serial_parts(serial: str):
    from core.database import Extern
    Extern.TestInfo.delete().where(Extern.TestInfo.serial == serial).execute()


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
    from core.database import Extern

    testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
    testInfo.save()


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

    fails = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial))
    
    for fail in fails:
        if fixture_id != fail.fixture_id and fail_reason == fail.fail_reason:
            return True

    return False