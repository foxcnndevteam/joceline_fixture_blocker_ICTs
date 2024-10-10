import peewee
from Manager.ConfigManager import ConfigManager
from Db.Models import Fixture
from Views.BlockedWindow import BlockedWindow
from env import BASE_DIR

class FixtureManager:

    def __init__(self):
        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, online=True)
            self.fixture.save()
        except peewee.IntegrityError:
            self.fixture = Fixture().select().where(Fixture.fixture_id == "HR001").get()

        cm = ConfigManager()

        self.maxFailCount = cm.getMaxFailCount()
        self.sfcPath = cm.getSFCPath()


    # --- Setters --- #

    def setOnline(self, isOnline: bool):
        self.fixture.online = isOnline
        self.fixture.save()

    def setSteps(self, steps: int):
        self.fixture.steps_count = steps
        self.fixture.save()

    def resetFailCount(self):
        self.fixture.fail_count = 0
        self.fixture.save()

    def resetStepsCount(self):
        self.setSteps(0)


    # --- Getters --- #

    def isOnline(self):
        return self.fixture.online
    
    def getFailCount(self):
        return self.fixture.fail_count
    
    
    # --- Utils --- #

    def incrementFixtureFails(self):
        self.fixture.fail_count += 1
        self.fixture.save()

    def incrementFixtureSteps(self):
        self.fixture.steps_count += 1
        self.fixture.save()

    def incrementFixtureSteps(self):
        self.fixture.steps_count += 1
        self.fixture.save()

    def resetFailCountIfPass(self, isPass: bool):
        if isPass:
            self.resetFailCount()


    # --- Listeners --- #

    def onTestSave(self, result: str, isFlowFBT: bool, params):
        self.incrementFixtureSteps()

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
        # params.insert(0, self.sfcPath)
        # subprocess.run(params)
        pass