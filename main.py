import typer
import os
import psutil
from Manager.FixtureManager import FixtureManager
from Manager.UserManager import UserManager
from Manager.ConfigManager import ConfigManager
from typing import List

app = typer.Typer(add_completion=False)

config = typer.Typer()
reset = typer.Typer()
set = typer.Typer()
get = typer.Typer()
test = typer.Typer()

set.add_typer(config, name="config")

app.add_typer(reset, name="reset")
app.add_typer(set, name="set")
app.add_typer(test, name="test")
app.add_typer(get, name="get")

fm = FixtureManager()
um = UserManager()
cm = ConfigManager()

@test.command()
def saveresult(result: str, isflowfbt: str, serial: str, failreason: str, fixtureid: str, sfcparams: List[str] = typer.Argument(None)):
    isflowfbt = isflowfbt.lower() in ("true")

    fm.onTestSave(result, isflowfbt, serial, failreason, fixtureid, sfcparams)

@test.command()
def chksn(sfcparams: List[str] = typer.Argument(None)):
    if fm.isOnline():
        fm.executeSFC(sfcparams)
    else:
        print("Test is running in offline mode --- PASS")

@app.command()
def createsuperuser(username: str, password: str):
    um.createSuperUser(username, password)

@reset.command()
def failcount():
    if um.authUser() == "PASS":
        fm.resetFailCount()
        print("Fail count has been reset")

@reset.command()
def stepscount():
    if um.authUser() == "PASS":
        fm.resetStepsCount()
        print("Steps count has been reset")

# --- Set commands --- #

@set.command()
def stepscount(steps: int):
    if um.authUser() == "PASS":
        fm.setSteps(steps)
        print("The steps where set")

@set.command()
def failcount(failcount):
    if um.authUser() == "PASS":
        fm.setFailCount(failcount)
        print("The fail count where set")

# --- Get commands --- #

@get.command()
def stepscount():
    print("Steps count: " + str(fm.getStepsCount()))

@get.command()
def failcount():
    print("Fails count: " + str(fm.getFailCount()))

# --- Config Commands --- #

@config.command()
def maxfailcount(maxfailcount: int):
    if um.authUser() == "PASS":
        cm.setMaxFailCount(maxfailcount)
        print("The max fail count where set")

@config.command()
def maxstepscount(maxstepscount: int):
    if um.authUser() == "PASS":
        cm.setMaxFailCount(maxstepscount)
        print("The max steps count where set")

@config.command()
def pctu(pass_count_to_unlock: int):
    if um.authUser() == "PASS":
        cm.setPassCountToUnlock(pass_count_to_unlock)
        print("The pass count to unlock fixture when steps fail where set")

# --- test debug command ---#

@app.command()
def testprogram():
    ppid = os.getppid()
    print(psutil.Process(ppid).name())

if __name__ == "__main__":
    app()