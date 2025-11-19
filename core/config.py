import os
import sys
import json
import peewee
from pathlib import Path
from typing import Literal, Any

from env import BASE_DIR
from utils import logger
from core.database import Models
from pydantic import BaseModel, ValidationError, PositiveInt, Field

class ExternalConfigSchema(BaseModel):
    unlock: PositiveInt = Field(gt=1, lt=6)
    block: PositiveInt = Field(ge=1, lt=6)
    ask_on_fail_mode: Literal["no", "partial", "full"]
    parts: str

data: Models.Local.Config

fixture_id = 'AF'

station="anon"

operation_mode:Literal['DEFAULT', 'RMA'] = 'DEFAULT'

t3 = False

ssh_key = None

config_g = {
    "unlock": 1,
    "block": 3,
    "ask_on_fail_mode": "no",
    "parts": ""
}

def load_external_config():
    global config_g, station, ssh_key

    try:
        from core.api.server_conn import get_config
        station_config = get_config(station, ssh_key)
        if station_config == None:
            return
        val_schema = ExternalConfigSchema(**station_config)
        config_g = json.loads(val_schema.model_dump_json())
    except ValidationError as e:
        print("invalid external config")
        

'''
#   Function: load_raw_config
#   Desc: Loads config file an checks if it exist or is corrupted.
'''
def load_raw_config() -> dict:
    raw_data = {}
    configFileName = "jocelinefb.conf.json"
    configFilePath = os.path.join(BASE_DIR, configFileName)

    if not os.path.isfile(configFilePath): 
        logger.error("Missing 'Configuration (jocelinefb.conf.json)' file")
        sys.exit(0)

    with open(configFilePath, 'r') as file:
        try: 
            raw_data = json.loads(file.read())
        except json.decoder.JSONDecodeError:
            logger.error("Corrupted configuration file: JSONDecodeError")
            sys.exit(0)
        file.close()

    return raw_data

def set_raw_config(key: str, value: Any):
    error: None | str = None
    raw_data = {}
    configFileName = "jocelinefb.conf.json"
    configFilePath = os.path.join(BASE_DIR, configFileName)

    if not os.path.isfile(configFilePath): 
        error = "config file not found"
        return error

    with open(configFilePath, 'r') as filer:
        try: 
            raw_data = json.loads(filer.read())
        except json.decoder.JSONDecodeError:
            error = "Corrupted configuration file: JSONDecodeError"
            # sys.exit(0)
        filer.close()

    raw_data[key] = value

    with open(configFilePath, 'w') as filew:
        json.dump(raw_data, filew, indent=4, separators=(',', ': '))
        filew.close()
    return error

'''
#   Function: load_config
#   Desc: Gets the config json file decoded, gets and loads all config keys.
'''
def load_config():
    global data, fixture_id, ssh_key, operation_mode, t3, station
    raw_data = load_raw_config()

    try:
        language = raw_data["lang"]
        extern_db_path = raw_data["extern_db_path"]
        server_log_path = raw_data["server_log_path"]

        boards_on_fixture_map = str(raw_data["boards_on_fixture_map"])
        udp_server_port = raw_data['udp_server_port']

    except KeyError as e:
        logger.error(f'Corrupted configuration file: Missing key "{e.args[0]}" in configuration file')
        sys.exit(0)
    try:
        station = raw_data["station"]
    except KeyError as e:
        print("station not setted")
    try:
        fixture_id = raw_data['fixture_id']
        ssh_key = raw_data.get('ssh_key')
        rma_mode = raw_data.get('rma_mode')
        if rma_mode == True:
            operation_mode = 'RMA'
        else:
            operation_mode = 'DEFAULT'
        t3j = raw_data.get('3t')
        if t3j != None:
            try:
                t3 = bool(t3j)
            except ValueError:
                print("bad value in t3")
    except KeyError as e:
        print("failed to get fixture id")

    try:
        data = Models.Local.Config(
            config_id = 0, 
            max_fail_count = 3, 
            block_pass = "R!ser2",
            language = language,
            extern_db_path = extern_db_path,
            server_log_path = server_log_path,
            boards_on_fixture_map = boards_on_fixture_map,
            test_count = 0,
            udp_server_port = udp_server_port,
            online_mode = True,
            pause_on_fail = False
        )

        data.save()
        logger.info("Configuration loaded first time")

    except peewee.IntegrityError:
        data = Models.Local.Config().select().where(Models.Local.Config.config_id == 0).get()
        data.language = language
        data.extern_db_path = extern_db_path
        data.server_log_path = server_log_path
        data.boards_on_fixture_map = boards_on_fixture_map
        data.udp_server_port = udp_server_port
        data.save()
    load_external_config()



# --- Getters --- #

def get_station() -> str:
    global station
    return station

def get_fixture_id() -> str:
    global fixture_id
    return fixture_id

def get_ask_fail_mode() -> str:
    global config_g
    return config_g["ask_on_fail_mode"]

def get_parts() -> str:
    global config_g
    return config_g["parts"]

def get_unlock_quantity():
    global config_g
    return config_g["unlock"]

def getMaxFailCount():
    global data, config_g
    return config_g["block"]
    
def getBlockPassword():
    global data
    return data.block_pass

def getLanguage():
    global data
    return data.language

def getExternDbPath():
    global data
    return data.extern_db_path

def getServerLogPath():
    global data
    return data.server_log_path

def get_test_count():
    global data
    return data.test_count

def getBoardsOnFixtureMap():
    global data
    return data.boards_on_fixture_map

def gey_yield_calc_qty():
    global data
    return data.yield_calc_quantity

def get_yield_block_threshold():
    global data
    return data.yield_block_threshold

def get_udp_server_port():
    global data
    return data.udp_server_port

def get_pause_on_fail():
    global data
    return data.pause_on_fail

def get_online_mode():
    global data
    return data.online_mode

def get_operation_mode() -> Literal['DEFAULT', 'RMA']:
    global operation_mode
    return operation_mode

def get_rma_mode() -> bool:
    global operation_mode
    return operation_mode == 'RMA'

def get_force_3t() -> bool:
    global t3
    return t3

# --- Setters --- #

def setMaxFailCount(maxFailCount: int):
    global data
    data.max_fail_count = maxFailCount
    data.save()

def setBlockPassword(blockPassword):
    global data
    data.block_pass = blockPassword
    data.save()

def increment_test_count():
    global data
    data.test_count = data.test_count + 1
    data.save()
    
def set_yield_calc_qty(yield_calc_quantity: int):
    global data
    data.yield_calc_quantity = yield_calc_quantity
    data.save()

def set_yield_block_threshold(yield_block_threshold: int):
    global data
    data.yield_block_threshold = yield_block_threshold
    data.save()

def set_pause_on_fail(pause_on_fail: bool):
    global data
    data.pause_on_fail = pause_on_fail
    data.save()

def set_online_mode(online_mode: bool):
    global data
    data.online_mode = online_mode
    data.save()

def set_rma_mode(new_value: bool):
    set_raw_config('rma_mode', new_value)
    load_config()
