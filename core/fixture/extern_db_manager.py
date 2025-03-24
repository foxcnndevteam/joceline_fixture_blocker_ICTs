def remove_serial_parts(serial: str):
    from core.database import Extern
    Extern.TestInfo.delete().where(Extern.TestInfo.serial == serial).execute()

def save_part_failed(result, serial, fixture_id, fail_reason = None):
    from core.database import Extern

    testInfo = Extern.TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
    testInfo.save()

def shouldUploadResult(serial, fixture_id, fail_reason):
    from core.database import Extern

    fails = list(Extern.TestInfo.select(Extern.TestInfo.fixture_id, Extern.TestInfo.fail_reason).where(Extern.TestInfo.serial == serial))
    
    for fail in fails:
        if fixture_id != fail.fixture_id and fail_reason == fail.fail_reason:
            return True

    return False