import os
import re
import sys
import logger

from env import BASE_DIR

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


class DevicesFinder:
    RESULT_FILE_NAME = "last_result.log"

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
    
