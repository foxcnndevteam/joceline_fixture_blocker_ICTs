import peewee
import subprocess
from Manager.ConfigManager import ConfigManager
from Db.Models import Fixture
from Db.Models import TestInfo
from Views.BlockedWindow import BlockedWindow
from Views.RetestWindow import RetestWindow
from env import BASE_DIR
from rich import print

class FixtureManager:

    def __init__(self):
        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
            self.fixture.save()
            print("debug")
        except peewee.IntegrityError:
            self.fixture = Fixture().select().where(Fixture.fixture_id == "HR001").get()

        cm = ConfigManager()

        self.maxFailCount = cm.getMaxFailCount()
        self.maxStepsCount = cm.getMaxStepsCount()
        self.pctu = cm.getPCTU()
        self.sfcPath = cm.getSFCPath()
        self.sfc_mode = cm.getSFCMode()

    def vacio(self):
        pass


    # --- Setters --- #

    def setOnline(self, isOnline: bool):
        self.fixture.online = isOnline
        self.fixture.save()

    def setSteps(self, steps: int):
        self.fixture.steps_count = steps
        self.fixture.save()

    def setPassCount(self, pass_count):
        self.fixture.pass_count = pass_count
        self.fixture.save()

    def setFailCount(self, fail_count):
        self.fixture.fail_count = fail_count
        self.fixture.save()

    def resetFailCount(self):
        self.setFailCount(0)

    def resetPassCount(self):
        self.setPassCount(0)

    def resetStepsCount(self):
        self.setSteps(0)


    # --- Getters --- #

    def isOnline(self):
        return self.fixture.online
    
    def getFailCount(self):
        return self.fixture.fail_count
    
    def getStepsCount(self):
        return self.fixture.steps_count
    
    def getPassCount(self):
        return self.fixture.pass_count
    
    
    # --- Utils --- #

    def incrementFixtureFails(self):
        self.fixture.fail_count += 1
        self.fixture.save()

    def incrementFixtureSteps(self):
        self.fixture.steps_count += 1
        self.fixture.save()

    def incrementFixturePass(self):
        self.fixture.pass_count += 1
        self.fixture.save()

    def resetFailCountIfPass(self, isPass: bool):
        if isPass:
            self.resetFailCount()


    # --- Listeners --- #

    def onTestSave(self, result: str, serial: str, fail_reason: str, fixture_id: str, params):
        if self.isOnline():
            self.saveTestInfo(result, serial, fail_reason, fixture_id)

            if result == "FAIL" and self.shouldUploadResult(serial):
                self.executeSFC(params)
                print("Result uploaded to SFC")
            elif result == "PASS":
                self.executeSFC(params)
                print("Result uploaded to SFC")
            else:
                retestWindow = RetestWindow()
                retestWindow.open()

                self.resetFailCountIfPass(result == "PASS")

        else:
            if result == "PASS":
                self.setOnline(True)
                self.resetFailCount()
                print("Fixture unlocked")
            else:
                print("Fixture status is locked")
            
        if result == "FAIL":
            self.incrementFixtureFails()

            if self.isMaxFailsReached():
                self.setOnline(False)
                blockWindow = BlockedWindow("failsLimitReached")
                blockWindow.open()
                print("Max fail count reached")


    # -- Verifiers --- #

    def isMaxFailsReached(self):
        if self.getFailCount() >= self.maxFailCount:
            return True
        
        return False
    

    # --- SFC --- #

    def executeSFC(self, params):
        params.insert(0, self.sfcPath)
        subprocess.run(params)

    def saveTestInfo(self, result, serial, fail_reason, fixture_id):
        if result == "PASS":
            TestInfo.delete().where(TestInfo.serial == serial).execute()
        else:
            testInfo = TestInfo(serial = serial, fail_reason = fail_reason, fixture_id = fixture_id)
            testInfo.save()

    def shouldUploadResult(self, serial):
        fails = list(TestInfo.select().where(TestInfo.serial == serial))

        for fail in fails:
            for fail2nd in fails:
                if fail.fixture_id != fail2nd.fixture_id and fail.fail_reason == fail2nd.fail_reason:
                    return True
                
        return False