import json
from Utils.MessageLoader import getMessages
from rich import print

class ConfLoader:

    def __init__(self):
        self.messages = getMessages()

        try:
            file = open("jfblocker.conf.json", "r")
        except FileNotFoundError:
            print(self.messages["error"]["confNotFound"])
            exit()

        data = json.load(file)
        
        print(data)

       
            
