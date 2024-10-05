import os
import json
import subprocess
from Utils.ConfLoader import ConfLoader
from Views.BlockedWindow import BlockedWindow
from env import BASE_DIR

class FixtureManager:
    dbName = "fixtureInfo.json"

    def __init__(self):
        if not os.path.isfile(os.path.join(BASE_DIR, self.dbName)):
            self.createFixtureInfo()

        self.loadFixtureInfo()

    def executeSFC(self, conf: ConfLoader, args):
        args.insert(0, conf.sfcPath)
        subprocess.run(args)

    def loadFixtureInfo(self):
        with open(os.path.join(BASE_DIR, self.dbName), 'r') as f:
            self.fixtureInfo = json.load(f)


    def createFixtureInfo(self):
        initialData = {
            "failCount": 0,
            "stepsCount": 0
        }

        open(os.path.join(BASE_DIR, self.dbName), 'x')

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(initialData, f)


    def setSteps(self, steps: int):
        self.fixtureInfo["stepsCount"] = steps

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(self.fixtureInfo, f)

    def incrementFailCount(self):
        self.fixtureInfo["failCount"] += 1

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(self.fixtureInfo, f)


    def incrementStepsCount(self):
        self.fixtureInfo["stepsCount"] += 1

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(self.fixtureInfo, f)


    def restartFailCount(self):
        self.fixtureInfo["failCount"] = 0

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(self.fixtureInfo, f)

    
    def restartStepsCount(self):
        self.fixtureInfo["stepsCount"] = 0

        with open(os.path.join(BASE_DIR, self.dbName), 'w') as f:
            json.dump(self.fixtureInfo, f)


    def shouldChangeBoard(self):
        if self.fixtureInfo["stepsCount"] >= 500:
            self.reasonCode = "stepsLimitReached"
            return True
        return False
    

    def shouldBlockByFails(self, conf: ConfLoader):
        if self.fixtureInfo["failCount"] >= conf.maxFailCount:
            self.reasonCode = "failsLimitReached"
            return True
        return False
    
    def chkFixStatus(self, conf: ConfLoader):
        if self.fixtureInfo["stepsCount"] >= 500:
            self.reasonCode = "stepsLimitReached"
            return "offline"
        elif self.fixtureInfo["failCount"] >= conf.maxFailCount:
            self.reasonCode = "failsLimitReached"
            return "offline"
        else:
            return "online"
        
    def blockFixture(self):
        blockedWindow = BlockedWindow(self.reasonCode)
        blockedWindow.open()