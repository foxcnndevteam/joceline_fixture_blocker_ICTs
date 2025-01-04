import sys
import peewee
import logger
import getpass
import Utils.lang as lang
import Db.Models as Models

from rich import print


def getUserMessages():
    try:
        return lang.messages["user"]
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)

def verifyAdminUserExist():
    try:
        newUser = Models.Local.User(username = "admin", password = "PsWaDMin12$")
        newUser.save()
    except peewee.IntegrityError:
        pass

def createSuperUser(username: str, password: str):
    verifyAdminUserExist()
    und_messages = getUserMessages()

    try:
        user_messages = {
            'created': und_messages['created'],
            'error': {
                'password_length': und_messages['error']['password_length'],
                'user_in_db': und_messages['error']['user_in_db']
            }
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)

    try:
        if authUser() == "PASS":
            if isSecurePassword(password):
                newUser = Models.Local.User(username = username, password = password)
                newUser.save()
                logger.info(user_messages["created"])
            else:
                logger.error(user_messages["error"]["password_length"])
    except peewee.IntegrityError:
        logger.error(user_messages["error"]["user_in_db"])


# --- Verifiers --- #

def isSecurePassword(password: str):
    if len(password) >= 8:
        return True
    return False
    
def authUser():
    verifyAdminUserExist()
    und_messages = getUserMessages()

    try:
        user_messages = {
            'login': und_messages['login'],
            'bad_login': und_messages['bad_login']
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)

    print(f'[bold]{user_messages["login"]}[/bold]')

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        user = Models.Local.User().select().where(Models.Local.User.username == username).get()
        if user.password == password:
            return "PASS"
        else:
            logger.error(user_messages["bad_login"])
    except peewee.DoesNotExist:
        logger.error(user_messages["bad_login"])

