from timeit import default_timer as timer
from datetime import timedelta

start = timer()

import sys
import cli
# import gui
import atexit
import logger

import Utils.lang as lang

import Manager.config as config
import core.fixture as fixture

is_window: bool = (len(sys.argv) < 2)

# --- Exit handler --- #
# Used to save logs when app exit
def exit_handler():
    logger.saveLogs()
    print()
    
    end = timer()
    print(timedelta(seconds=end-start))

# --- Initial data & Config loader --- #
def load_inital_data():
    config.load_config()
    lang.loadMessages()
    fixture.load_fixture_info()

def main():
    try:
        load_inital_data()
            
        # ~ Alternate between window or cli mode
        if is_window:
            # exit_code = gui.execute()
            exit_code = 0
        else:
            exit_code = cli.exec_()
        
        sys.exit(exit_code)
    
    except Exception as e:
        try:
            logger.error(lang.messages["unexpected_error"])
            print(e)
        except KeyError as e:
            logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
            logger.error('An unexpected error occurred, please contact support team')
        logger.crash(f'FATAL_ERROR: {e.args}')
        sys.exit(1)

if __name__ == "__main__":
    atexit.register(exit_handler)
    main()
