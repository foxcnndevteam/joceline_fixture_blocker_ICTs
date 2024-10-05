import typer
from Utils.FixtureManager import FixtureManager

# from Utils.ConfLoader import ConfLoader
# from Db.FixtureManager import FixtureManager

app = typer.Typer(add_completion=False)
fm = FixtureManager()
# conf = ConfLoader()

@app.command()
def savetestresult(result: str, isflowfbt: str):
    isflowfbt = isflowfbt.lower() in ("true")

    fm.onTestSave(result, isflowfbt, 0)
# def savetestresult(result: str, serialnumber: str, operatorid: str, fixtureid: str, location: str, errorcode: str, log: str, passchksn: str):
#     fm.incrementStepsCount()

#     if result == "FAIL" and passchksn == "true":
#         fm.incrementFailCount()

#     if fm.chkFixStatus(conf) == "online":
#         if result == "PASS":
#             fm.restartFailCount()
#         if passchksn == "true":
#             fm.executeSFC(conf, ["u", serialnumber, operatorid, fixtureid, location, errorcode, log])
#         else:
#             print("Upload SFC Skipped")
#     elif fm.chkFixStatus(conf) == "offline" and result == "PASS" and not fm.shouldChangeBoard():
#         fm.restartFailCount()
#         print("Fixture is unlocked")
#     else:
#         fm.blockFixture()

@app.command()
def chksn(serialnumber: str, operatorid: str, fixtureid: str, location: str):
    pass
#     if fm.chkFixStatus(conf) == "offline":
#         print("Test is running in offline mode --- PASS")
#     else:
#         fm.executeSFC(conf, ["c", serialnumber, operatorid, fixtureid, location])

# @app.command()
# def restartfailcount():
#     fm.restartFailCount()

# @app.command()
# def restartstepscount():
#     fm.restartStepsCount()

# @app.command()
# def setsteps(steps: int):
#     fm.setSteps(steps)

if __name__ == "__main__":
    app()


# import sys
# manager = FixtureManager()

# manager.resetStepsCount()