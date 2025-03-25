import os
import sys
import json

from env import BASE_DIR

from core import config
from utils import logger

messages = []

def load_messages():
    global messages
    
    messagesFileName = f'messages-{config.getLanguage()}.json'
    messagesFilePath = os.path.join(BASE_DIR, "lang", messagesFileName)

    if not os.path.isfile(messagesFilePath): 
        logger.error(f'Missing \'Lang ({messagesFileName})\' file')
        sys.exit(0)

    with open(messagesFilePath, "r", encoding='utf-8') as file:
        try:
            messages = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            logger.error("Corrupted messages file: JSONDecodeError")
            sys.exit(0)
