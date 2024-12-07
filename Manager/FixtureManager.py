import peewee
import subprocess
import os
from Manager.ConfigManager import ConfigManager
from Db.Models import Fixture
from Db.Models import TestInfo
from env import BASE_DIR
from rich import print
from Utils.LogParser import extractFailedPartsInLog

class FixtureManager:

    def __init__(self):
        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
            self.fixture.save()
        except peewee.IntegrityError:
            self.fixture = Fixture().select().where(Fixture.fixture_id == "HR001").get()

        cm = ConfigManager()

        self.maxFailCount = cm.getMaxFailCount()

    def vacio(self):
        pass


    # --- Setters --- #

    def setOnline(self, isOnline: bool):
        self.fixture.online = isOnline
        self.fixture.save()

    def setFailCount(self, fail_count):
        self.fixture.fail_count = fail_count
        self.fixture.save()

    def resetFailCount(self):
        self.setFailCount(0)


    # --- Getters --- #

    def isOnline(self):
        return self.fixture.online
    
    def getFailCount(self):
        return self.fixture.fail_count
    
    
    # --- Utils --- #

    def incrementFixtureFails(self):
        self.fixture.fail_count += 1
        self.fixture.save()

    def resetFailCountIfPass(self, isPass: bool):
        if isPass:
            self.resetFailCount()
    
    def saveRetestResultInPath(self, result: str):
        with open(os.path.join(BASE_DIR, "retest_result.txt"), "w") as f:
            f.write(result)

    def saveOnlineResultInPath(self):
        with open(os.path.join(BASE_DIR, "online_result.txt"), "w") as f:
            f.write(str(self.isOnline()))


    # --- Listeners --- #

    def onTestSave(self, result: str, serial: str, fixture_id: str, fail_status: int):
        
        partsFailed = extractFailedPartsInLog(fail_status)
        print(partsFailed)

        i = 1
        for partFailed in partsFailed:

            if self.isOnline():
                self.saveTestInfo(result, serial, partFailed, fixture_id)

                self.resetFailCountIfPass(result == "PASS" or result == "PASSED")

                if partFailed == "OTF" or ((result == "FAIL" or result == "FAILED") and self.shouldUploadResult(serial)):
                    self.saveRetestResultInPath("False")
                    print("Result uploaded to SFC")
                    break
                elif result == "PASS" or result == "PASSED":
                    self.saveRetestResultInPath("False")
                    print("Result uploaded to SFC")
                    break
                elif i >= len(partsFailed):
                    subprocess.run([str(os.path.join(BASE_DIR, "JocelineFB.exe")), 'window', 'open', 'retestView'])
                    self.saveRetestResultInPath("True")

            else:
                if result == "PASS" or result == "PASSED":
                    self.setOnline(True)
                    self.resetFailCount()
                    print("Fixture unlocked")
                    break
                else:
                    print("Fixture status is locked")
                    break
            
            i += 1
            
        if result == "FAIL" or result == "FAILED":
            self.incrementFixtureFails()

            if self.isMaxFailsReached():
                self.setOnline(False)
                subprocess.run([str(os.path.join(BASE_DIR, "JocelineFB.exe")), 'window', 'open', 'blockedView'])
                print("Max fail count reached")


    # -- Verifiers --- #

    def isMaxFailsReached(self):
        if self.getFailCount() >= self.maxFailCount:
            return True
        
        return False
    

    # --- SFC --- #

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