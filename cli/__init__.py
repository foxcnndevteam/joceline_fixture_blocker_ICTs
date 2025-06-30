import sys
import click

from env import VERSION_PROGRAM

from utils import lang, logger
from core import user, fixture, config as config_manager, api
from cli.views import window
from udpsocket import client
from utils.help_printer import get_help

# --- Main group ---- #
@click.group()
def app():
    pass

# --- Setup CLI --- #
def setup_cli():
    print()

    # --- Commands groups --- #
    @app.group()
    def set():
        pass

    @app.group()
    def get():
        pass

    @app.group()
    def test():
        pass

    @set.group()
    def config():
        pass



    # --------------------- Main commands --------------------- #
    '''
    #    Command: createsuperuser
    #    Usage: JocelineFB.exe createsuperuser <username:str> <password:str>
    #    Desc: Used to create admin users who can modify app settings.
    '''
    @app.command()
    @click.argument('username')
    @click.argument('password')
    def createsuperuser(username, password):
        user.createSuperUser(username, password)



    # --------------------- Test commands --------------------- #
    '''
    #    Command: test saveresult
    #    Usage: JocelineFB.exe test saveresult <result:PASS|FAIL> <serial:str> <fixtureid:str> <failstatus:int>
    #    Desc: Used to save and process test info. Also if is only one board auto check status.
    '''
    @test.command()
    @click.argument('result', type=str)
    @click.argument('serial', type=str)
    @click.argument('fixtureid', type=str)
    @click.argument('failstatus', type=int)
    def saveresult(result, serial, fixtureid, failstatus):
        
        # ~ This is an option to modify loggger settings when is executed in test.
        logger.save_log_as_test(
            props_to_add={
                'serial': serial,
                'result': result,
                'fixtureid': fixtureid
            }
        )
        
        # ~ Send info to process
        fixture.process_info(result, serial, fixtureid, failstatus)

    @test.command()
    @click.argument('result', type=str)
    @click.argument('serial', type=str)
    @click.argument('fixtureid', type=str)
    @click.argument('failstatus', type=int)
    @click.argument('projectname', type=str)
    @click.argument('projectmodel', type=str)
    @click.argument('operatorid', type=str)
    @click.argument('sku', type=str)
    @click.argument('testname', type=str)
    @click.argument('ipaddress', type=str)
    @click.argument('logname', type=str)
    @click.argument('teststarttime', type=str)
    @click.argument('testendtime', type=str)
    @click.argument('testdurationseconds', type=str)
    def saveresult2(result, serial, fixtureid, failstatus, projectname, projectmodel, operatorid, sku, testname, ipaddress, logname, teststarttime, testendtime, testdurationseconds):

        # ~ This is an option to modify loggger settings when is executed in test.
        logger.save_log_as_test(
            props_to_add={
                'serial': serial,
                'result': result,
                'fixtureid': fixtureid
            }
        )
        
        execution_mode = "ONLINE"
        if fixture.get_fixture_state(False) == 'Offline':
            execution_mode = "OFFLINE"

        fixture.process_info_2(result, serial, fixtureid, failstatus, projectname, projectmodel, operatorid, sku, "host", testname, execution_mode, ipaddress, logname, teststarttime, testendtime, testdurationseconds)

    '''
    #    Command: test checkstatus
    #    Usage: JocelineFB.exe test checkstatus
    #    Desc: Used to check and save fixture status when multiple boards
    '''
    @test.command()
    def checkstatus():
        config_manager.increment_test_count()
        fixture.check_retest_status()
        fixture.check_block_status_alt(False)
        client.send_update_signal()
        window.openWindows()



    # --------------------- Config commands --------------------- #
    '''
    #    Command: set failcount
    #    Usage: JocelineFB.exe set failcount <failcount:int>
    #    Desc: Used to modify fixture fail count
    '''
    @set.command()
    @click.argument('failcount', type=int)
    def failcount(failcount):
        if user.authUser() == "PASS":
            fixture.set_fail_count(failcount)
            try:
                logger.info(lang.messages["setter"]["fail_count"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)



    '''
    #    Command: get failcount
    #    Usage: JocelineFB.exe get failcount
    #    Desc: Used get current fixture fail count
    '''
    @get.command()
    def failcount():
        click.echo(f"Fails count: {fixture.get_fail_count()}")



    '''
    #    Command: get fixturestatus
    #    Usage: JocelineFB.exe get fixturestatus 
    #    Desc: Used to save and display fixture status
    '''
    @get.command()
    def fixturestatus():
        fixture.save_online_result_in_path()
        fixture.save_should_pause_in_path()
        click.echo(f"Fixture online status: {fixture.is_online() and config_manager.get_online_mode()}")



    '''
    #    Command: set config maxfailcount
    #    Usage: JocelineFB.exe set config maxfailcount <maxfailcount:int>
    #    Desc: Used to modify fixture max fail count
    '''
    @config.command()
    @click.argument('maxfailcount', type=int)
    def maxfailcount(maxfailcount):
        if user.authUser() == "PASS":
            config_manager.setMaxFailCount(maxfailcount)
            try:
                logger.info(lang.messages["setter"]["max_fail_count"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)



    '''
    #    Command: set config yieldcalcqty
    #    Usage: JocelineFB.exe set config yieldcalcqty <yield_calc_quantity:int>
    #    Desc: Used to modify fixture yield calc quantity
    '''
    @config.command()
    @click.argument('yield_calc_quantity', type=int)
    def yieldcalcqty(yield_calc_quantity):
        if user.authUser() == "PASS":
            config_manager.set_yield_calc_qty(yield_calc_quantity)
            try:
                logger.info(lang.messages["setter"]["yield_calc_quantity"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)



    '''
    #    Command: set config yieldblockthr
    #    Usage: JocelineFB.exe set config yieldblockthr <yield_block_threshold:int>
    #    Desc: Used to modify fixture yield block threshold
    '''
    @config.command()
    @click.argument('yield_block_threshold', type=int)
    def yieldblockthr(yield_block_threshold):
        if user.authUser() == "PASS":
            config_manager.set_yield_block_threshold(yield_block_threshold)
            try:
                logger.info(lang.messages["setter"]["yield_block_threshold"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)



    '''
    #    Command: set config blockpassword
    #    Usage: JocelineFB.exe set config blockpassword <newpassword:str>
    #    Desc: Used to modify fixture block password
    '''
    @config.command()
    @click.argument('newpassword', type=str)
    def blockpassword(newpassword):
        if user.authUser() == "PASS":
            config_manager.setBlockPassword(newpassword)
            try:
                logger.info(lang.messages["setter"]["block_password"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

    '''
    #    Command: shouldpause
    #    Usage: JocelineFB.exe shouldpause
    #    Desc: Eval if it should pause during in the test on fail
    '''
    @app.command()
    def shouldpause():
        print(fixture.get_pause_on_fail())

    '''
    #    Command: fixturestate
    #    Usage: JocelineFB.exe fixturestate
    #    Desc: get the state of the fixture
    '''
    @app.command()
    def fixturestate():
        state = fixture.get_fixture_state(False)
        online = 0
        if state == 'Online':
            online = 1
        print(online)


    @app.command()
    def sshtunnel():
        is_alive = api.eval_tunnel_conection()

        if not is_alive:
            api.create_tunnel_ssh()
            print("SSH tunnel created")
        else:
            print("SSH tunnel already created")

    '''
    #    Command: help
    #    Usage: JocelineFB.exe help
    #    Desc: show all available commands
    '''
    @app.command()
    def help():
        get_help()

    '''
    #    Command: version
    #    Usage: JocelineFB.exe version
    #    Desc: Show the version of the program
    '''
    @app.command()
    def version():
        print(f"v{VERSION_PROGRAM}")


# --- Execute CLI --- #
def exec_():
    setup_cli()
    exit_code = app(standalone_mode=False)
    
    return exit_code