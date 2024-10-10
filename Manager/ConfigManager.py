import peewee
import json
import os
from Db.Models import Config
from env import BASE_DIR

class ConfigManager: 
    
    confFileName = "jocelinefb.conf.json"

    def __init__(self):
        try:
            with open(os.path.join(BASE_DIR, self.confFileName), 'r') as file:
                confFile = json.loads(file.read())
            sfcPath = confFile["sfcPath"]

            self.config = Config(configId = 0, max_fail_count = 2, max_steps_count = 500, pctu_steps_lock = 3, sfc_path = sfcPath)
            self.config.save()
        except peewee.IntegrityError:
            self.config = Config().select().where(Config.configId == 0).get()


    # --- Getters --- #

    def getSFCPath(self):
        return self.config.sfc_path
    
    def getMaxFailCount(self):
        return self.config.max_fail_count
    
    
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