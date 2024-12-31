import os
import datetime
import traceback
from typing import List
from env import BASE_DIR

class ReportFiles:
    DATE: str = datetime.datetime.now().replace(microsecond=0).isoformat()[:19]

    INFO_LOG_PATH: str = os.path.join(BASE_DIR, "reports")
    ERROR_LOG_PATH: str = os.path.join(BASE_DIR, "reports", "crash")

    CRASH_REPORT_FILENAME: str = f"CRASH_REPORT_{DATE}.log".replace(':', "-")
    INFO_REPORT_FILENAME: str = f"LOG_REPORT_{DATE}.log".replace(':', "-")

class Levels:
    INFO: str = "INFO"
    WARNING: str = "WARNING"
    ERROR: str = "ERROR"
    DEBUG: str = "DEBUG"

PROGRAM: str = "JocelineFB"

ERROR_LOG_RESULT: List[str] = []
INFO_LOG_RESULT: List[str] = []

def configureLogger():
    if not os.path.exists(ReportFiles.INFO_LOG_PATH): os.makedirs(ReportFiles.INFO_LOG_PATH)
    if not os.path.exists(ReportFiles.ERROR_LOG_PATH): os.makedirs(ReportFiles.ERROR_LOG_PATH)

def writeLog(path: str, log_result: List[str], filename: str):
    str_result = ''.join(str(f"{line}\n") for line in log_result)

    with open(os.path.join(path, filename), 'a') as f:
        f.write(str_result)


def info(message: str):
    INFO_LOG_RESULT.append(
        f"{Levels.INFO}:{PROGRAM}:{message}"
    )

def warning(message: str):
    INFO_LOG_RESULT.append(
        f"{Levels.WARNING}:{PROGRAM}:{message}"
    )

def debug(message: str):
    INFO_LOG_RESULT.append(
        f"{Levels.DEBUG}:{PROGRAM}:{message}"
    )

def error(error_title: str):
    separator = ("*" * 100) + '\n' + ("*" * 100) + '\n'

    ERROR_LOG_RESULT.append(
        f"{separator}{Levels.ERROR}:{PROGRAM}:{error_title}\n{traceback.format_exc()}"
    )

def saveLogs():
    if len(INFO_LOG_RESULT) > 0: writeLog(ReportFiles.INFO_LOG_PATH, INFO_LOG_RESULT, ReportFiles.INFO_REPORT_FILENAME)
    if len(ERROR_LOG_RESULT) > 0: writeLog(ReportFiles.ERROR_LOG_PATH, ERROR_LOG_RESULT, ReportFiles.CRASH_REPORT_FILENAME)
    # writeLog(INFO_LOG_RESULT)
    # print(len(ERROR_LOG_RESULT))
    # pass

# def configure_logging():
#     logpath = os.path.join(BASE_DIR, "reports")
#     if not os.path.exists(logpath):
#         os.makedirs(logpath)

#     date = str(datetime.datetime.now().replace(microsecond=0).isoformat())[:19]
#     filename = f"CRASH_REPORT_{date}.log".replace(':', "-")

#     logging.basicConfig(filename=f"./reports/{filename}", level=logging.ERROR)

#     filename = f"INFO_REPORT_{date}.log".replace(':', "-")

#     logging.basicConfig(filename=f"./reports/{filename}", level=logging.INFO)



