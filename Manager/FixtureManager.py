import peewee
import subprocess
import os
import re
from Manager.ConfigManager import ConfigManager
from Db.Models import Fixture
from Db.Models import TestInfo
from env import BASE_DIR
from rich import print

class FixtureManager:

    def __init__(self):
        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, pass_count=0, online=True)
            self.fixture.save()
        except peewee.IntegrityError:
            self.fixture = Fixture().select().where(Fixture.fixture_id == "HR001").get()

        cm = ConfigManager()

        self.maxFailCount = cm.getMaxFailCount()
        self.maxStepsCount = cm.getMaxStepsCount()
        self.pctu = cm.getPCTU()
        self.sfcPath = cm.getSFCPath()
        #self.sfc_mode = cm.getSFCMode()


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

    def extractFailedParts(self):
        failed_parts = []
        with open(os.path.join(BASE_DIR, "last_result.log"), 'r') as file:
            for line in file:
                matches = re.findall(r"(\S+?) HAS FAILED", line)
                if matches:
                    failed_parts.extend(matches)
        return failed_parts
    
    def saveRetestResultInPath(self, result: str):
        with open(os.path.join(BASE_DIR, "retest_result.txt"), "w") as f:
            f.write(result)

    def saveOnlineResultInPath(self):
        with open(os.path.join(BASE_DIR, "online_result.txt"), "w") as f:
            f.write(str(self.isOnline()))


    # --- Listeners --- #

    def onTestSave(self, result: str, serial: str, fixture_id: str, fail_status: int):
        
        if fail_status == 1010:
            partsFailed = self.extractFailedParts()
        else:
            partsFailed = ["OTF"]

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
                else:
                    subprocess.run([str(os.path.join(BASE_DIR, "JocelineFB.exe")), 'window', 'open', 'retestView'])
                    self.saveRetestResultInPath("True")
                    break

            else:
                if result == "PASS" or result == "PASSED":
                    self.setOnline(True)
                    self.resetFailCount()
                    print("Fixture unlocked")
                    break
                else:
                    print("Fixture status is locked")
                    break
            
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