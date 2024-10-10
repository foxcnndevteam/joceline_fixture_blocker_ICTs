import peewee
import getpass
from Db.Models import User

class UserManager:

    def __init__(self):
        try:
            newUser = User(username = "admin", password = "PsWaDMin12$")
            newUser.save()
        except peewee.IntegrityError:
            pass


    # --- Getters --- #

    def getUserRole(self, username: str):
        try:
            user = User().select().where(User.username == username).get()
            return user.role
        except peewee.DoesNotExist:
            return "ERROR"
            

    # --- User creator taking a unique user --- #

    def createSuperUser(self, username: str, password: str):
        try:
            if self.authUser() == "PASS":
                if self.isSecurePassword(password):
                    newUser = User(username = username, password = password)
                    newUser.save()
                    print("User was created successfully")
                else:
                    print("Error: Password must be a minimum of 8 characthers")
            
        except peewee.IntegrityError:
            print("Error: User already in the database")


    # --- Verifiers --- #

    def isSecurePassword(self, password: str):
        if len(password) >= 8:
            return True
        return False
    
    def authUser(self):
        print("To do it you must be an administrator, please log in.")
        username = input("Username: ")
        password = getpass.getpass("Password: ")

        try:
            user = User().select().where(User.username == username).get()
            if user.password == password:
                return "PASS"
            else:
                print("Error: Bad login")
        except peewee.DoesNotExist:
            print("Error: Bad login")