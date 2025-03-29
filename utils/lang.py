import os
import sys
import json

from env import BASE_DIR

from core import config
from utils import logger

# ~ Global messages saved on RAM
messages = []
'''
#   Function: load_messages
#   Desc: Read messages file and save it in messages.
'''
def load_messages():
    global messages
    
    # ~ Defines messages filename and path
    messagesFileName = f'messages-{config.getLanguage()}.json'
    messagesFilePath = os.path.join(BASE_DIR, "lang", messagesFileName)

    # ~ Checks if messages file exist
    if not os.path.isfile(messagesFilePath): 
        logger.error(f'Missing \'Lang ({messagesFileName})\' file')
        sys.exit(0)

    # ~ Opens messages and decodes it.
    with open(messagesFilePath, "r", encoding='utf-8') as file:
        try:
            messages = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            logger.error("Corrupted messages file: JSONDecodeError")
            sys.exit(0)
