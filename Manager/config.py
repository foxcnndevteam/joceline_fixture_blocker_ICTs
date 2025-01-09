import os
import sys
import json
import logger
import peewee
import Db.Models as Models

from env import BASE_DIR


data: Models.Local.Config

configFileName = "jocelinefb.conf.json"
configFilePath = os.path.join(BASE_DIR, configFileName)

raw_data = []

def loadRawConfig():
    global raw_data
    global configFileName
    global configFilePath

    if not os.path.isfile(configFilePath): 
        logger.error("Missing 'Configuration (jocelinefb.conf.json)' file")
        sys.exit(0)

    with open(configFilePath, 'r') as file:
        try: 
            raw_config_data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            logger.error("Corrupted configuration file: JSONDecodeError")
            sys.exit(0)

    raw_data = raw_config_data

def loadConfigInDb():
    global data

    try:
        language = raw_data["lang"]
        extern_db_path = raw_data["extern_db_path"]
        boards_on_fixture_map = str(raw_data["boards_on_fixture_map"])

    except KeyError as e:
        logger.error(f'Corrupted configuration file: Missing key "{e.args[0]}" in configuration file')
        sys.exit(0)

    try:
        data = Models.Local.Config(
            config_id = 0, 
            max_fail_count = 2, 
            block_pass = "R!ser2",
            language = language,
            extern_db_path = extern_db_path,
            boards_on_fixture_map = boards_on_fixture_map
        )

        data.save()
        logger.info("Configuration loaded first time")

    except peewee.IntegrityError:
        data = Models.Local.Config().select().where(Models.Local.Config.config_id == 0).get()
        data.language = language
        data.extern_db_path = extern_db_path
        data.boards_on_fixture_map = boards_on_fixture_map
        data.save()



# --- Getters --- #

def getMaxFailCount():
    global data
    return data.max_fail_count
    
def getBlockPassword():
    global data
    return data.block_pass

def getLanguage():
    global data
    return data.language

def getExternDbPath():
    global data
    return data.extern_db_path

def getBoardsOnFixtureMap():
    global data
    return data.boards_on_fixture_map

# --- Setters --- #

def setMaxFailCount(maxFailCount: int):
    global data
    data.max_fail_count = maxFailCount
    data.save()

def setBlockPassword(blockPassword):
    global data
    data.block_pass = blockPassword
    data.save()
