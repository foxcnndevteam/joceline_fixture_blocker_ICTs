import os
import datetime
import traceback

from rich import print
from typing import List
from env import BASE_DIR

datetime_now = datetime.datetime.now()


class ReportFiles:
    DATE: str = datetime.datetime.now().replace(microsecond=0).isoformat()[:19]

    INFO_LOG_PATH: str = os.path.join(BASE_DIR, "reports")
    CRASH_LOG_PATH: str = os.path.join(BASE_DIR, "reports", "crash")

    INFO_REPORT_FILENAME: str = f"LOG_REPORT_{DATE}.log".replace(':', "-")
    CRASH_REPORT_FILENAME: str = f"CRASH_REPORT_{DATE}.log".replace(':', "-")

class Levels:
    INFO: str = "INFO"
    ERROR: str = "ERROR"
    CRASH: str = "CRASH"
    DEBUG: str = "DEBUG"
    WARNING: str = "WARNING"


PROGRAM: str = "JocelineFB"

INFO_LOG_RESULT: List[str] = []
CRASH_LOG_RESULT: List[str] = []

def info(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'[bold]Info:[/bold] {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.INFO}]:{PROGRAM}:{message}"
    )

def debug(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'[bold #949494]Debug:[/bold #949494] {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.DEBUG}]:{PROGRAM}:{message}"
    )

def error(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'

    print(f'[bold red]Error:[/bold red] {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.ERROR}]:{PROGRAM}:{message}"
    )

def warning(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'[bold #bbc000]Warning:[/bold #bbc000] {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.WARNING}]:{PROGRAM}:{message}"
    )

def crash(crash_title: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    CRASH_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.CRASH}]:{PROGRAM}:{crash_title}\n{traceback.format_exc()}"
    )

def writeLog(path: str, log_result: List[str], filename: str):
    str_result = ''.join(str(f"{line}\n") for line in log_result)

    with open(os.path.join(path, filename), 'a') as f:
        f.write(str_result)

def configureLogger():
    if not os.path.exists(ReportFiles.INFO_LOG_PATH): os.makedirs(ReportFiles.INFO_LOG_PATH)
    if not os.path.exists(ReportFiles.CRASH_LOG_PATH): os.makedirs(ReportFiles.CRASH_LOG_PATH)

def saveLogs():
    if len(INFO_LOG_RESULT) > 0: writeLog(ReportFiles.INFO_LOG_PATH, INFO_LOG_RESULT, ReportFiles.INFO_REPORT_FILENAME)
    if len(CRASH_LOG_RESULT) > 0: writeLog(ReportFiles.CRASH_LOG_PATH, CRASH_LOG_RESULT, ReportFiles.CRASH_REPORT_FILENAME)

