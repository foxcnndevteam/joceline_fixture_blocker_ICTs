import os
import re
from env import BASE_DIR

def extractFailedPartsInLog(fail_status: int):
    failed_parts = []

    parts_by_hf = DevicesFinder.byHasFailed()
    parts_by_hf = [f"{fail_status}-{part}" for part in parts_by_hf]

    parts_by_shorts = DevicesFinder.byOpenShort()
    parts_by_shorts = [f"{fail_status}-{part}" for part in parts_by_shorts]
    parts_by_testjet = []
    testjet_failed_devices = DevicesFinder.byKeyAfter("Device")
    testjet_failed_pins = DevicesFinder.byKeyAfter("Pin")

    if len(testjet_failed_devices) == len(testjet_failed_pins):
        for i in range(0, len(testjet_failed_devices)):
            parts_by_testjet.append (f"{fail_status}-{testjet_failed_devices[i]}-{testjet_failed_pins[i]}")

    failed_parts = parts_by_hf + parts_by_shorts + parts_by_testjet

    if len(failed_parts) == 0:
        return ["OTF"]
    return failed_parts


class DevicesFinder:
    RESULT_FILE_NAME = "last_result.log"

    @staticmethod
    def byOpenShort():
        failed_parts = []

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            data = file.read()
    
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

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            for line in file:
                matches = re.findall(r"(\S+?) HAS FAILED", line)
                if matches:
                    failed_parts.extend(f"HF-{comp}" for comp in matches)
        return failed_parts

    @staticmethod
    def byKeyAfter(strKey: str):
        failed_parts = []

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            for line in file:
                matches = re.findall(r" " + strKey + r" (\S+)", line)
                if matches:
                    failed_parts.extend(f"{strKey}-{comp}" for comp in matches)
        return failed_parts
    
    @staticmethod
    def byDevicesInParallel():
        failed_parts = []

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            data = file.read()
    
        sections = data.split('----------------------------------------')
            
        for section in sections:
            match = re.search(r'DEVICES IN PARALLEL\s*(.*?)$', section, re.DOTALL)
            if match:
                devices_block = match.group(1)

                devices = [line.strip() for line in devices_block.splitlines() if line.strip()]

                if devices:
                    failed_parts.extend([f"DIP-{device}" for device in devices])
                else:
                    failed_parts.append(f"DIP-GENERAL")

        return failed_parts



class Utils:

    @staticmethod
    def getFailCode():

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            for line in file:
                matches = re.findall(r":(.+?)\s* test:FAILED", line)

                if matches:
                    return matches[0]
                
    def getBoard():

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            for line in file:
                matches = re.findall(r"Board_Description:(\S+)", line)
                if matches:
                    return matches[0][0:3]










