import json
from Utils.MessageLoader import getMessages
from rich import print
import os
from env import BASE_DIR

class ConfLoader:
    confName = "jocelinefb.conf.json"

    def __init__(self):
        self.messages = getMessages()

        try:
            file = open(os.path.join(BASE_DIR, self.confName), "r")
        except FileNotFoundError:
            print(self.messages["error"]["confNotFound"])
            exit()

        data = json.load(file)

        self.maxFailCount = data["maxFailCount"]
        self.sfcPath = data["sfcPath"]