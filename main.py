import sys
import typer
import logger
import atexit
import Utils.lang as lang
import Manager.user as user
import Manager.config as config
import Manager.boards as boards
import Manager.fixture as fixture

from rich import print
from Views.RetestWindow  import RetestWindow
from Views.BlockedWindow import BlockedWindow


# --- Exit handler --- #
# Used to save logs when app exit

def exit_handler():
    logger.saveLogs()
    print()
atexit.register(exit_handler)


# --- App start --- #

def startAppData():
    logger.configureLogger()
    config.loadRawConfig()
    config.loadConfigInDb()
    lang.loadMessages()
    fixture.loadFixtureInfo()
    boards.loadBoardsInfo()

try:
    app = typer.Typer(add_completion=False)

    set_command = typer.Typer()
    get_command = typer.Typer()
    test_command = typer.Typer()
    config_command = typer.Typer()
    window_command = typer.Typer()


    app.add_typer(set_command, name="set")
    app.add_typer(get_command, name="get")
    app.add_typer(test_command, name="test")
    app.add_typer(window_command, name="window")
    set_command.add_typer(config_command, name="config")

    @test_command.command()
    def saveresult( result: str, serial: str, fixtureid: str, failstatus: int):
        fixture.onTestSave( result, serial, fixtureid, failstatus )

    @app.command()
    def createsuperuser( username: str, password: str ):
        user.createSuperUser( username, password )

    @app.command()
    def savefixtureonline():
        fixture.saveOnlineResultInPath()

#     # --- Set commands --- #

    @set_command.command()
    def failcount( failcount ):
        if user.authUser() == "PASS":
            fixture.setFailCount( failcount )
            try:
                logger.info(lang.messages["setter"]["fail_count"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

#     # --- Get commands --- #

    @get_command.command()
    def failcount():
        print( "[bold]Fails count:[/bold] " + str( fixture.getFailCount() ) )

#     # --- Config Commands --- #

    @config_command.command()
    def maxfailcount( maxfailcount: int ):
        if user.authUser() == "PASS":
            config.setMaxFailCount( maxfailcount )
            try:
                logger.info(lang.messages["setter"]["max_fail_count"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

    @config_command.command()
    def blockpassword( newpassword: str ):
        if user.authUser() == "PASS":
            config.setBlockPassword( newpassword )
            try:
                logger.info(lang.messages["setter"]["block_password"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

#     # --- window commands --- #

    @window_command.command()
    def open( view: str):
        if view == "blockedView":
            pass
            blockWindow = BlockedWindow("failsLimitReached")
            blockWindow.open()
        elif view == "retestView":
            retestWindow = RetestWindow()
            retestWindow.open()
        else:
            try:
                logger.error(lang.messages["view_not_exist"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

    # --- test debug command ---#

    # @app.command()
    # def testprogram():
    #     boards.fixtureHasFails()

    if __name__ == "__main__":
        print()
        startAppData()
        app()

except Exception as e:
    try:
        logger.error(lang.messages["unexpected_error"])
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        logger.error('An unexpected error occurred, please contact support team')
    logger.crash(f'FATAL_ERROR: {e.args}') 
