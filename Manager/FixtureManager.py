import peewee
import subprocess
from Manager.ConfigManager import ConfigManager
from Db.Models import Fixture
from Views.BlockedWindow import BlockedWindow
from env import BASE_DIR

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

    def resetFailCount(self):
        self.fixture.fail_count = 0
        self.fixture.save()

    def resetPassCount(self):
        self.fixture.pass_count = 0
        self.fixture.save()

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

    def onTestSave(self, result: str, isFlowFBT: bool, params):
        self.incrementFixtureSteps()

        if self.getStepsCount() >= self.maxStepsCount:
            self.setOnline(False)

            if self.getPassCount() == 0:
                window = BlockedWindow("stepsLimitReached")
                window.open()
                print("Max steps count reached")
                self.setPassCount(1)
                return

            if result == "PASS":
                self.incrementFixturePass()
            elif result == "FAIL":
                self.setPassCount(1)

            if self.getPassCount() >= (self.pctu + 1):
                self.resetStepsCount()
                self.resetPassCount()
                self.setOnline(True)
                print("Fixture unlocked")
            else:
                print("Pass number: " + str(self.getPassCount() - 1))
            
            return
        else:
            self.resetPassCount()



        if isFlowFBT:
            if self.isOnline():
                self.executeSFC(params)
                self.resetFailCountIfPass(result == "PASS")
                print("Result uploaded to SFC")

            else:
                if result == "PASS":
                    self.setOnline(True)
                    print("Fixture unlocked")
                else:
                    print("Fixture status is locked")
            
            if result == "FAIL":
                self.incrementFixtureFails()

                if self.isMaxFailsReached():
                    self.setOnline(False)
                    window = BlockedWindow("failsLimitReached")
                    window.open()
                    print("Max fail count reached")

        else:
            print("The MB is not FBT")


    # -- Verifiers --- #

    def isMaxFailsReached(self):
        if self.getFailCount() >= self.maxFailCount:
            return True
        
        return False
    

    # --- SFC --- #

    def executeSFC(self, params):
        params.insert(0, self.sfcPath)
        subprocess.run(params)