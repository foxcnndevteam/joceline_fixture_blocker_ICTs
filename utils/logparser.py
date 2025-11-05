import os
import re
import sys
from pathlib import Path

from utils import logger
from env import BASE_DIR

def read_hex_byte(char: str):
    char_byte = bytes.fromhex(char)
    try:
        return char_byte.decode("UTF-8")
    except UnicodeDecodeError:
        return '.'

serial_fru_regex = re.compile(r'Serial :[0-9A-Z]{17}')
serial_mem_regex = re.compile(r'0x[A-F0-9]{6} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2} [A-F0-9]{2}')
# byte_hex_regex = re.compile(r'[A-F0-9]{2}')
serial_fru_regex_mac = re.compile(r'Serial :[0-9A-Z]{17}_[A-F0-9]{12}')

def read_memory_fru(content: str, serial:str) -> bool:
    
    memory_raw = ""
    memory_raw_search = serial_mem_regex.findall(content)
    for mem_r in memory_raw_search:
        memory_raw += re.sub(r'0x000[0-1][0-9A-F]0', "", mem_r)
    memory = memory_raw.split(" ")

    serial_fru_mem = ""
    caracter = 0
    len_str = len(serial)
    for byte in memory:
        decoded = read_hex_byte(byte.replace(" ", ""))
        if caracter == len_str:
            break
        if decoded == serial[caracter]:
            serial_fru_mem = serial_fru_mem + decoded
            caracter += 1
        else:
            serial_fru_mem = ""
            caracter = 0
    
    return serial_fru_mem == serial

def is_fru_correct(serial: str) -> dict:
    serial_fru = ""

    file_path = os.path.join(BASE_DIR, "fru.txt")
    if not Path(file_path).exists():
        return { "is_correct": True, "found": False }
    with open(file_path, "r") as f:
        content = f.read()
        f.close()
        search_serial_fru = serial_fru_regex.findall(content)
        serial_fru = search_serial_fru[0].split(":")[1]
        serial_fru_correct = serial == serial_fru
        fru_found_memory = read_memory_fru(content, serial)
        os.remove(file_path)
        return { "is_correct": serial_fru_correct and fru_found_memory, "found": True }

def read_mac_memory(content: str, mac:str) -> bool:

    memory_raw = ""
    memory_raw_search = serial_mem_regex.findall(content)
    for mem_r in memory_raw_search:
        memory_raw += re.sub(r'0x[A-F0-9]{6}', "", mem_r)
    memory_arr = memory_raw.split(" ")

    memory = ""
    for byte in memory_arr:
        memory = memory + byte
    return memory.startswith(mac)

def is_mac_correct() -> dict:
    mac = ""

    file_path = os.path.join(BASE_DIR, "mac.txt")
    if not Path(file_path).exists():
        return { "is_correct": False, "found": False }
    with open(file_path, "r") as f:
        content = f.read()
        f.close()
        serial_mac = serial_fru_regex_mac.findall(content)
        mac = serial_mac[0].split("_")[1]
        mac_correct = read_mac_memory(content, mac)
        os.remove(file_path)
        return { "is_correct": mac_correct, "found": True }

def is_mac_fru_valid(serial: str) -> dict:
    fru_result = is_fru_correct(serial)
    mac_result = is_mac_correct()

    if fru_result["found"] and mac_result["found"]:
        return { "result": fru_result["is_correct"] and mac_result["is_correct"], "found": fru_result["found"] and mac_result["found"]}

    if fru_result["found"]:
        return { "result": fru_result["is_correct"], "found": fru_result["found"] }

    if mac_result["found"]:
        return { "result": mac_result["is_correct"], "found": mac_result["found"] }

    return { "result": True, "found": False }

'''
#   Function: extractFailedPartsInLog
#   Desc: Extracts fail devices in log by fail_status
#   Arguments:
#       fail_status | type:int | Status code to extract devices.
'''
def extractFailedPartsInLog(fail_status: int):

    failed_parts = []

    # --- Finds board failed parts by "HAS FAILED" wordkey ------------------------------ #
    parts_by_hf = DevicesFinder.byHasFailed()
    parts_by_hf = [f"{fail_status}-{part}" for part in parts_by_hf]


    # --- Finds board failed parts by "common Devices" list ----------------------------- #
    parts_by_shorts = DevicesFinder.byOpenShort()
    parts_by_shorts = [f"{fail_status}-{part}" for part in parts_by_shorts]


     # --- Finds board failed parts by "Device" & "Pin" wordkey ------------------------- #
    parts_by_testjet = []
    testjet_failed_devices = DevicesFinder.byKeyAfter("Device")
    testjet_failed_pins = DevicesFinder.byKeyAfter("Pin")

    if len(testjet_failed_devices) == len(testjet_failed_pins):
        for i in range(0, len(testjet_failed_devices)):
            parts_by_testjet.append (f"{fail_status}-{testjet_failed_devices[i]}-{testjet_failed_pins[i]}")


    # --- Appends all lists in only one list -------------------------------------------- #
    failed_parts = parts_by_hf + parts_by_shorts + parts_by_testjet

    if len(failed_parts) == 0:
        return ["OTF"]
    return failed_parts


'''
#   Class: DevicesFinder
#   Desc: Contains the static methods to extract by regex var the failed devices.
'''
class DevicesFinder:
    RESULT_FILE_NAME = "last_result.log"

    '''
    #   Function: byOpenShort
    #   Desc: Extracts fail devices by open or short keyword.
    '''
    @staticmethod
    def byOpenShort():
        failed_parts = []

        try:
            with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
                data = file.read()
        except FileNotFoundError:
            logger.error('Missing \'Result (last_result.log)\' file')
            sys.exit(0)
    
        sections = data.split('----------------------------------------')
        
        for section in sections:

            if "Pin " in section:
                failed_parts = []
                break

            if "Open #" in section:
                prefix = "OPEN"
            elif "Short #" in section:
                prefix = "SHORT"
            else:
                continue
                
            match = re.search(r'Common Devices:\s*(.*?)(?:Too many to print|Message|Total of|------End|$)', section, re.DOTALL)
            if match:
                devices_block = match.group(1)
                
                devices = [line.strip() for line in devices_block.splitlines() if line.strip()]
                
                if devices:
                    failed_parts.extend([f"{prefix}-{device}" for device in devices])
                else:
                    failed_parts.append(f"{prefix}-GENERAL")
            else: 
                failed_parts.append(f"{prefix}-GENERAL")

        return failed_parts
    
    
    '''
    #   Function: byHasFailed
    #   Desc: Extracts fail devices by has failed keyword.
    '''
    @staticmethod
    def byHasFailed():
        failed_parts = []

        try:
            with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
                for line in file:
                    matches = re.findall(r"(\S+?) HAS FAILED", line)
                    if matches:
                        failed_parts.extend(f"HF-{comp}" for comp in matches)
        except FileNotFoundError:
            logger.error('Missing \'Result (last_result.log)\' file')
            sys.exit(0)

        return failed_parts

    
    '''
    #   Function: byKeyAfter
    #   Desc: Extracts fail devices by after some keyword.
    '''
    @staticmethod
    def byKeyAfter(strKey: str):
        failed_parts = []

        try:
            with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
                for line in file:
                    matches = re.findall(r" " + strKey + r" (\S+)", line)
                    if matches:
                        failed_parts.extend(f"{strKey}-{comp}" for comp in matches)
        except FileNotFoundError:
            logger.error('Missing \'Result (last_result.log)\' file')
            sys.exit(0)

        return failed_parts
    
