import peewee
import json
import os
from Db.Models import Config
from env import BASE_DIR

class ConfigManager: 
    
    confFileName = "jocelinefb.conf.json"

    def __init__(self):
        with open(os.path.join(BASE_DIR, self.confFileName), 'r') as file:
            confFile = json.loads(file.read())

        sfc_mode = confFile["sfc"]["sfc_mode"]
        binaryPath = confFile["sfc"]["binaryPath"]
        apiUrl = confFile["sfc"]["apiUrl"]

        sfcPath = confFile["sfcPath"]
        
        try:
            self.config = Config(configId = 0, max_fail_count = 2, max_steps_count = 500, pctu_steps_lock = 4, sfc_path = sfcPath)
            self.config.save()
        except peewee.IntegrityError:
            self.config = Config().select().where(Config.configId == 0).get()

            self.config.sfc_mode = sfc_mode
            self.config.binaryPath = binaryPath
            self.config.apiUrl = apiUrl

            self.config.sfc_path = sfcPath
            self.config.save()


    # --- Getters --- #

    def getSFCPath(self):
        return self.config.sfc_path
    
    def getSFCMode(self):
        return self.config.sfc_mode
    
    def getBinaryPath(self):
        return self.config.binaryPath
    
    def getApiUrl(self):
        return self.config.apiUrl
    
    def getMaxFailCount(self):
        return self.config.max_fail_count
    
    def getMaxStepsCount(self):
        return self.config.max_steps_count
    
    def getPCTU(self):
        return self.config.pctu_steps_lock
    
    
    # --- Setters --- #

    def setMaxFailCount(self, maxFailCount: int):
        self.config.max_fail_count = maxFailCount
        self.config.save()

    def setMaxStepsCount(self, maxStepsCount: int):
        self.config.max_fail_count = maxStepsCount
        self.config.save()

    def setPassCountToUnlock(self, passCountToUnlock: int):
        self.config.pctu_steps_lock = passCountToUnlock
        self.config.save()