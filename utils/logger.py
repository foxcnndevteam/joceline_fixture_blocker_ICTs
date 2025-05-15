import os
import shutil
import datetime
import traceback

from core import config
from typing import List
from env import BASE_DIR

# ~ Gets current timestamp
datetime_now = datetime.datetime.now()

'''
#   Class: ReportFiles
#   Desc: Defines the metadata of reports files.
'''
class ReportFiles:
    DATE: str = datetime.datetime.now().replace(microsecond=0).isoformat()[:19]
    # ~ Value to indicates if should be uploaded to server path.
    SAVE_ON_SERVER: bool = False

    FIXTURE_ID: str = ''
    INFO_LOG_PATH: str = os.path.join(BASE_DIR, "reports")
    CRASH_LOG_PATH: str = os.path.join(BASE_DIR, "reports", "crash")

    INFO_REPORT_FILENAME: str = f"LOG_REPORT_{DATE}.txt".replace(':', "-")
    CRASH_REPORT_FILENAME: str = f"CRASH_REPORT_{DATE}.txt".replace(':', "-")


'''
#   Class: Levels
#   Desc: Defines the level str prefix.
'''
class Levels:
    INFO: str = "INFO"
    ERROR: str = "ERROR"
    CRASH: str = "CRASH"
    DEBUG: str = "DEBUG"
    WARNING: str = "WARNING"


# ~ Defines the program name to show like prefix in log.
PROGRAM: str = "JocelineFB"


# ~ These arrays saves the log lines.
INFO_LOG_RESULT: List[str] = []
CRASH_LOG_RESULT: List[str] = []


'''
#   Function: info
#   Desc: Adds prefixs to the info message saved in info array lines.
#   Arguments:
#       message | type:str | Line or message will be save in log array.
'''
def info(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'Info: {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.INFO}]:{PROGRAM}:{message}"
    )


'''
#   Function: debug
#   Desc: Adds prefixs to the debug message saved in info array lines.
#   Arguments:
#       message | type:str | Line or message will be save in log array.
'''
def debug(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'Debug: {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.DEBUG}]:{PROGRAM}:{message}"
    )


'''
#   Function: error
#   Desc: Adds prefixs to the error message saved in info array lines.
#   Arguments:
#       message | type:str | Line or message will be save in log array.
'''
def error(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'

    print(f'Error: {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.ERROR}]:{PROGRAM}:{message}"
    )


'''
#   Function: warning
#   Desc: Adds prefixs to the warning message saved in info array lines.
#   Arguments:
#       message | type:str | Line or message will be save in log array.
'''
def warning(message: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    print(f'Warning: {message}')
    INFO_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.WARNING}]:{PROGRAM}:{message}"
    )


'''
#   Function: crash
#   Desc: Adds prefixs to the crash message saved in crash array lines.
#   Arguments:
#       message | type:str | Line or message will be save in crash array.
'''
def crash(crash_title: str):
    timestamp_date = f'{datetime_now.year}-{datetime_now.month}-{datetime_now.day}'
    timestamp_time = f'{datetime_now.hour}:{datetime_now.minute}:{datetime_now.second}'
    
    CRASH_LOG_RESULT.append(
        f"[{timestamp_date}]:[{timestamp_time}]:[{Levels.CRASH}]:{PROGRAM}:{crash_title}\n{traceback.format_exc()}"
    )


'''
#   Function: writeLog
#   Desc: Gets and parses lines to be saved in log or crash log files.
#   Arguments:
#       path       | type:str       | Path where save the log file.
#       log_result | type:List[str] | Lines will be save in log file.
#       filename   | type:str       | File name of the log file.
'''
def writeLog(path: str, log_result: List[str], filename: str, sub_directory: str = ''):
    # ~ Parses lines to add a new line between lines
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

        server_dir =  os.path.join(
                config.getServerLogPath(),
                sub_directory
            )
        if not os.path.exists(server_dir) and sub_directory != '':
            os.makedirs(server_dir, exist_ok=True)
        shutil.copyfile(
            os.path.join(
                path,
                filename
            ),
            os.path.join(server_dir, filename)
        )    

def check_reports_path():
    if not os.path.exists(ReportFiles.INFO_LOG_PATH): os.makedirs(ReportFiles.INFO_LOG_PATH)
    if not os.path.exists(ReportFiles.CRASH_LOG_PATH): os.makedirs(ReportFiles.CRASH_LOG_PATH)

def saveLogs():
    check_reports_path()
    
    if len(INFO_LOG_RESULT) > 0: writeLog(ReportFiles.INFO_LOG_PATH, INFO_LOG_RESULT, ReportFiles.INFO_REPORT_FILENAME, ReportFiles.FIXTURE_ID)
    if len(CRASH_LOG_RESULT) > 0: writeLog(ReportFiles.CRASH_LOG_PATH, CRASH_LOG_RESULT, ReportFiles.CRASH_REPORT_FILENAME)


def save_log_as_test(props_to_add):
    ReportFiles.INFO_REPORT_FILENAME = ReportFiles.INFO_REPORT_FILENAME[:-4]
    
    ReportFiles.SAVE_ON_SERVER = (props_to_add['result'] == 'FAIL')
    
    for prop in props_to_add.values():
        ReportFiles.INFO_REPORT_FILENAME += f'-{prop}'
    # ReportFiles.FIXTURE_ID = props_to_add['fixtureid']
    ReportFiles.INFO_REPORT_FILENAME += '.txt'