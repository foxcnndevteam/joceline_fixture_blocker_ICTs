import sys
import cli
import gui
import atexit

from utils import logger, lang
from core import config, fixture

# ~ If app doesn't get args the system up a window
is_window: bool = (len(sys.argv) < 2)

# --- Exit handler --- #
'''
#    Function: exit_handler
#    Desc: Used print last line and save all logs (Crash & Info)
'''
def exit_handler():
    logger.saveLogs()
    print()

# --- Initial data & Config loader --- #
'''
#    Function: load_inital_data
#    Desc: Used to load config, lang an fixture data
'''
def load_inital_data():
    config.load_config()
    lang.load_messages()
    fixture.load_fixture()
    
# --- Main app executer --- #
'''
#    Function: main
#    Desc: Initial function of system
'''
def main():
    try:
        load_inital_data()
        
        # ~ Alternate between window or cli mode
        if is_window:
            # ~ Execute gui and get exit code
            exit_code = gui.exec_()
        else:
            # ~ Execute cli and get exit code
            exit_code = cli.exec_()
        
        sys.exit(exit_code)
    
    except Exception as e:

        # ~ Receive an error message and, if received, display a generic error.
        
        try:
            logger.error(lang.messages["unexpected_error"])
            print(e)
        except KeyError as e:
            logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
            logger.error('An unexpected error occurred, please contact support team')
        
        logger.crash(f'FATAL_ERROR: {e.args}')
        sys.exit(1)





# ~ There start all
if __name__ == "__main__":
    
    # ~ Register the exit function and execute the system
    atexit.register(exit_handler)
    main()
