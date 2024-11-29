import os
import re
from env import BASE_DIR

def extractFailedPartsByStatus(fail_status: int):

    if fail_status == 1010:
        return getPreshortFails()
    elif fail_status == 1004:
        return getShortFails()
    else:
        return ["OTF"]
    

def getPreshortFails():
    STATUS = "1010"
    failed_parts = []

    with open(os.path.join(BASE_DIR, "last_result.log"), 'r') as file:
        for line in file:
            matches = re.findall(r"(\S+?) HAS FAILED", line)
            if matches:
                failed_parts.extend(f"{STATUS}-{comp}" for comp in matches)
    return failed_parts

def getShortFails():
    STATUS = "1004"
    failed_parts = []

    with open(os.path.join(BASE_DIR, "last_result.log"), 'r') as file:
        data = file.read()
    
    data = ''.join(str(e + "\n") for e in data.split('\n')[33:])
        
    sections = data.split('----------------------------------------')
        
    for section in sections:
        if "Open" in section:
            prefix = "OPEN"
        elif "Short" in section:
            prefix = "SHORT"
        else:
            continue
            
        match = re.search(r'Common Devices:\s*(.*?)(?:Too many to print|Message|Total of|------End|$)', section, re.DOTALL)
        if match:
            devices_block = match.group(1)
            
            devices = [line.strip() for line in devices_block.splitlines() if line.strip()]
            
            if devices:
                failed_parts.extend([f"{STATUS}-{prefix}-{device}" for device in devices])
            else:
                failed_parts.append(f"{STATUS}-{prefix}-GENERAL")
        else: 
            failed_parts.append(f"{STATUS}-{prefix}-GENERAL")

    return failed_parts