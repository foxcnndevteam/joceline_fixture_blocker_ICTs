import peewee
import os
import json
from Db.Models import Fixture
from env import BASE_DIR

class FixtureManager:

    confFileName = "joceline.conf.json"

    def __init__(self):

        try:
            self.fixture = Fixture(fixture_id="HR001", fail_count=0, steps_count=0, online=True)
            self.fixture.save()
        except peewee.IntegrityError:
            self.fixture = Fixture().select().where(Fixture.fixture_id == "HR001").get()

        with open(os.path.join(BASE_DIR, self.confFileName), 'r') as file:
            self.maxFailCount = json.loads(file)["maxFailCount"]

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

        if self.isOnline() and isFlowFBT:
            self.executeSFC()
            self.resetFailCountIfPass(result == "PASS")

        elif self.isOnline():
            print("SFC SKIPPED")

        elif not self.isOnline():
            self.setOnline(result == "PASS")

        if result == "FAIL":
            self.incrementFixtureFails()

    # -- Verifiers --- #

    # TODO
    def verifyMaxFailsReached():
        pass

    # --- SFC --- #

    def executeSFC(self):
        print("sfc executed")