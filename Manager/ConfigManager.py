import peewee
import json
import os
from Db.Models import Config
from env import BASE_DIR

class ConfigManager: 
    

    def __init__(self):
        try:
            self.config = Config(
                                    configId = 0, 
                                    max_fail_count = 2, 
                                    block_pass = "R!ser2"
                                )
            self.config.save()
        except peewee.IntegrityError:
            self.config = Config().select().where(Config.configId == 0).get()


    # --- Getters --- #

    def getMaxFailCount(self):
        return self.config.max_fail_count
    
    def getBlockPassword(self):
        return self.config.block_pass
    

    # --- Setters --- #

    def setMaxFailCount(self, maxFailCount: int):
        self.config.max_fail_count = maxFailCount
        self.config.save()

    def setBlockPassword(self, blockPassword):
        self.config.block_pass = blockPassword
