import os
import re
from env import BASE_DIR

def extractFailedPartsInLog(fail_status: int):

    error_code = Utils.getFailCode()
    print(error_code)

    if (
        (error_code == "Pre_shorts") or
        (error_code == "Setup power supply") or
        (error_code == "Boundary scan powered shorts") or
        (error_code == "Boundary scan interconnect") or
        (error_code == "Boundary scan connect") or
        (error_code == "Digital incircuit") or
        (error_code == "Analog functional") or
        (error_code == "Function")
    ):
        failed_parts = DevicesFinder.byHasFailed()
        failed_parts = [f"{fail_status}-{part}" for part in failed_parts]
        return failed_parts
    
    elif error_code == "Shorts":
        failed_parts = DevicesFinder.byOpenShort()
        failed_parts = [f"{fail_status}-{part}" for part in failed_parts]
        return failed_parts
    
    elif error_code == "Testjet":
        # #Option 1: Only with Device
        # failed_parts = DevicesFinder.byKeyAfter("Device")
        # failed_parts = [f"{fail_status}-{part}" for part in failed_parts]

        # #Option 2: Only with Pin
        # failed_parts = DevicesFinder.byKeyAfter("Pin")
        # failed_parts = [f"{fail_status}-{part}" for part in failed_parts]

        # #Option 3: Only with Node
        # failed_parts = DevicesFinder.byKeyAfter("Node")
        # failed_parts = [f"{fail_status}-{part}" for part in failed_parts]

        #Option 4: Combination between Device, Pin & Node
        failed_parts = []
        failed_devices = DevicesFinder.byKeyAfter("Device")
        failed_pins = DevicesFinder.byKeyAfter("Pin")
        failed_nodes = DevicesFinder.byKeyAfter("Node")

        for i in range(0, len(failed_devices)):
            failed_parts.append (f"{fail_status}-{failed_devices[i]}-{failed_pins[i]}-{failed_nodes[i]}")
        
        return failed_parts
    
    elif error_code == "Analog unpowered":
        # #Option 1: Only by HAS FAILED
        # failed_parts = DevicesFinder.byHasFailed()
        # failed_parts = [f"{fail_status}-{part}" for part in failed_parts]
        
        #Option 2: With devices in parallel
        failed_parts = DevicesFinder.byHasFailed()
        failed_in_parallel = DevicesFinder.byDevicesInParallel()

        failed_parts = failed_parts + failed_in_parallel
        failed_parts = [f"{fail_status}-{part}" for part in failed_parts]

        return failed_parts
    else:
        return ["OTF"]


class DevicesFinder:
    RESULT_FILE_NAME = "last_result.log"

    @staticmethod
    def byOpenShort():
        failed_parts = []

        with open(os.path.join(BASE_DIR, DevicesFinder.RESULT_FILE_NAME), 'r') as file:
            data = file.read()
    
        sections = data.split('----------------------------------------')
            
        for section in sections:
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










