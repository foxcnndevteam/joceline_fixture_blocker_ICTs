import os
import shutil
import datetime
import traceback
import core.config as config

from rich import print
from typing import List
from env import BASE_DIR

datetime_now = datetime.datetime.now()


class ReportFiles:
    DATE: str = datetime.datetime.now().replace(microsecond=0).isoformat()[:19]
    SAVE_ON_SERVER: bool = False

    INFO_LOG_PATH: str = os.path.join(BASE_DIR, "reports")
    CRASH_LOG_PATH: str = os.path.join(BASE_DIR, "reports", "crash")

    INFO_REPORT_FILENAME: str = f"LOG_REPORT_{DATE}.txt".replace(':', "-")
    CRASH_REPORT_FILENAME: str = f"CRASH_REPORT_{DATE}.txt".replace(':', "-")

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
        
    if ReportFiles.SAVE_ON_SERVER:
        info("------------------------ Config used ------------------------")
        info(f'Language: {config.data.language}')
        info(f'Extern DB path: {config.data.extern_db_path}')
        info(f'Server log path: {config.data.server_log_path}')
        info(f'Boards on fixture map: {config.data.boards_on_fixture_map}')
        info("-------------------------------------------------------------")

        shutil.copyfile(
            os.path.join(
                path,
                filename
            ),
            os.path.join(
                config.getServerLogPath(),
                filename
            )
        )    

def check_reports_path():
    if not os.path.exists(ReportFiles.INFO_LOG_PATH): os.makedirs(ReportFiles.INFO_LOG_PATH)
    if not os.path.exists(ReportFiles.CRASH_LOG_PATH): os.makedirs(ReportFiles.CRASH_LOG_PATH)

def saveLogs():
    check_reports_path()
    
    if len(INFO_LOG_RESULT) > 0: writeLog(ReportFiles.INFO_LOG_PATH, INFO_LOG_RESULT, ReportFiles.INFO_REPORT_FILENAME)
    if len(CRASH_LOG_RESULT) > 0: writeLog(ReportFiles.CRASH_LOG_PATH, CRASH_LOG_RESULT, ReportFiles.CRASH_REPORT_FILENAME)


def save_log_as_test(props_to_add):
    ReportFiles.INFO_REPORT_FILENAME = ReportFiles.INFO_REPORT_FILENAME[:-4]
    
    ReportFiles.SAVE_ON_SERVER = (props_to_add['result'] == 'FAIL')
    
    for prop in props_to_add.values():
        ReportFiles.INFO_REPORT_FILENAME += f'-{prop}'
    
    ReportFiles.INFO_REPORT_FILENAME += '.txt'