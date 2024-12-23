import datetime
import typer
import os
import logging
import psutil
import logger
import traceback
from Manager.FixtureManager import FixtureManager
from Manager.UserManager    import UserManager
from Manager.ConfigManager  import ConfigManager
from env import BASE_DIR
from Views.BlockedWindow import BlockedWindow
from Views.RetestWindow  import RetestWindow

# app_logging.configure_logging()

logger.configureLogger()

try:
    app = typer.Typer( add_completion=False )

    set    = typer.Typer()
    get    = typer.Typer()
    config = typer.Typer()
    test   = typer.Typer()
    window = typer.Typer()

    set.add_typer( config, name="config" )
    app.add_typer( set   , name="set"    )
    app.add_typer( test  , name="test"   )
    app.add_typer( get   , name="get"    )
    app.add_typer( window, name="window" )

    fm = FixtureManager()
    um = UserManager()
    cm = ConfigManager()

    @test.command()
    def saveresult( result: str, serial: str, fixtureid: str, failstatus: int ):
        fm.onTestSave( result, serial, fixtureid, failstatus )

    @app.command()
    def createsuperuser( username: str, password: str ):
        um.createSuperUser( username, password )

    @app.command()
    def savefixtureonline():
        fm.saveOnlineResultInPath()

    # --- Set commands --- #

    @set.command()
    def failcount( failcount ):
        if um.authUser() == "PASS":
            fm.setFailCount( failcount )
            print( "The fail count where set" )

    # --- Get commands --- #

    @get.command()
    def failcount():
        print( "Fails count: " + str( fm.getFailCount() ) )

    # --- Config Commands --- #

    @config.command()
    def maxfailcount( maxfailcount: int ):
        if um.authUser() == "PASS":
            cm.setMaxFailCount( maxfailcount )
            print( "The max fail count where set" )

    @config.command()
    def blockpassword( newpassword: str ):
        if um.authUser() == "PASS":
            cm.setBlockPassword( newpassword )
            print( "The block password where set" )

    # --- window commands --- #

    @window.command()
    def open( view: str ):
        if view == "blockedView":
            blockWindow = BlockedWindow("failsLimitReached")
            blockWindow.open()
        elif view == "retestView":
            retestWindow = RetestWindow()
            retestWindow.open()
        else:
            print("La view no existe")

    # --- test debug command ---#

    @app.command()
    def testprogram():
        ppid = os.getppid()
        print(psutil.Process(ppid).name())

    if __name__ == "__main__":
        app()
except Exception as e:
    # logging.info(traceback.format_exc())
    logger.error("ERROR PRINCIPAL")

logger.saveLogs()
