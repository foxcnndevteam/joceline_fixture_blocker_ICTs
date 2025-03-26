import sys
import peewee
import getpass

from utils import logger, lang
from core.database import Models

'''
#   Function: getUserMessages
#   Desc: This function is used to get the user messages node and check errors in the lang file.
'''
def getUserMessages():
    try:
        return {
            'created': lang.messages["user"]['created'],
            'error': {
                'password_length': lang.messages["user"]['error']['password_length'],
                'user_in_db': lang.messages["user"]['error']['user_in_db']
            },
            'login': lang.messages["user"]['login'],
            'bad_login': lang.messages["user"]['bad_login']
        }
    except KeyError as e:
        logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
        sys.exit(0)


'''
#   Function: verifyAdminUserExist
#   Desc: Used to check if admin user exist in database.
'''
def verifyAdminUserExist():
    try:
        newUser = Models.Local.User(username = "admin", password = "PsWaDMin12$")
        newUser.save()
    except peewee.IntegrityError:
        pass


'''
#   Function: createSuperUser
#   Desc: This function create a superuser like admin.
#   Arguments:
#       username      | type:str | User username
#       password      | type:str | User password
'''
def createSuperUser(username: str, password: str):
    verifyAdminUserExist()
    user_messages = getUserMessages()

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
'''
#   Function: isSecurePassword
#   Desc: Check if admin password leng to determinate if is scure to use.
#   Arguments:
#       password      | type:str | User password
'''
def isSecurePassword(password: str):
    if len(password) >= 8:
        return True
    return False
 

'''
#   Function: authUser
#   Desc: Authenticate user
'''
def authUser():
    verifyAdminUserExist()
    user_messages = getUserMessages()

    print(f'{user_messages["login"]}')

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

