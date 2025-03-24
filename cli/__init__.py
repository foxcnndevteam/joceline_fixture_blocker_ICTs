import sys
import click
import logger
import udpsocket

import Utils.lang as lang

import cli.views.window as window

import core.config as config_manager
import Manager.user as user
# import Manager.fixture as fixture
import core.fixture as fixture
import udpsocket.client

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
    #    Usage: JocelineFB createsuperuser <username:str> <password:str>
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
    #    Usage: JocelineFB test saveresult <result:PASS|FAIL> <serial:str> <fixtureid:str> <failstatus:int>
    #    Desc: Used to save and process test info. Also if is only one board auto check status.
    '''
    @test.command()
    @click.argument('result')
    @click.argument('serial')
    @click.argument('fixtureid')
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
    def checkstatus():
        config_manager.increment_test_count()
        fixture.check_retest_status()
        fixture.check_block_status()
        udpsocket.client.send_update_signal()
        window.openWindows()

    # --------------------- Config commands --------------------- #
    @set.command()
    @click.argument('failcount')
    def failcount(failcount):
        if user.authUser() == "PASS":
            fixture.set_fail_count(failcount)
            try:
                logger.info(lang.messages["setter"]["fail_count"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

    @get.command()
    def failcount():
        click.echo(f"[bold]Fails count:[/bold] {fixture.getFailCount()}")

    @get.command()
    def fixturestatus():
        fixture.save_online_result_in_path()
        click.echo(f"[bold]Fixture online status:[/bold] {fixture.is_online()}")

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

    @config.command()
    @click.argument('newpassword')
    def blockpassword(newpassword):
        if user.authUser() == "PASS":
            config_manager.setBlockPassword(newpassword)
            try:
                logger.info(lang.messages["setter"]["block_password"])
            except KeyError as e:
                logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
                sys.exit(0)

# --- Execute CLI --- #
def exec_():
    setup_cli()
    exit_code = app(standalone_mode=False)
    
    return exit_code