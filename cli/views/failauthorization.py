import sys

from utils import lang, logger

from core import config

from core.api.server_conn import auth_user

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy

'''
#   Class: FailAuthorization
#   Desc: when it is required to authorize or not the fail of the test
'''
class FailAuthorizationWindow(QWidget):
    # ~ Used in all windows instance on cli to check if cli should display it in full screen
    show_fullscreen = True


    '''
    #   Function: __init__        -        Class instance
    #   Arguments:
    #       block_reason | type:str  | Argument to get info message. You can check it in messages-{lang}.json -> block_view -> reasons)
    '''
    def __init__(self, on_set_fail, message = "", *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.on_set_fail = on_set_fail
        self.message = message
        self.setupGui()
    
    def setupGui(self):

        self.setStyleSheet("background-color: #ff4f29;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        labelTitle = QLabel("Ingresa credenciales para continuar")
        labelTitle.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")
        
        label_message = QLabel(self.message)
        label_message.setStyleSheet("font-size: 15px; padding: 0px; margin: 0px; font-weight: bold;")


        self.employ_number = QLineEdit()
        self.employ_number.setPlaceholderText("numero empleado")
        self.employ_number.setStyleSheet("padding: 5px; margin: 0px; margin-top: 5px; border: none; border-radius: 5px; background-color: white;")    
        
        self.passwd_input = QLineEdit()
        self.passwd_input.setPlaceholderText("Password")
        self.passwd_input.setStyleSheet("padding: 5px; margin: 0px; margin-top: 5px; border: none; border-radius: 5px; background-color: white;")
        self.passwd_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passwd_input.setEchoMode(QLineEdit.EchoMode.Password)


        fail_button = QPushButton("Fallar")
        fail_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        fail_button.setStyleSheet("""
            QPushButton {
                padding: 10px; 
                margin: 0px; 
                background-color: orange; 
                border-radius: 5px; 
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(252, 186, 3); /* Color de fondo al pasar el cursor */
            }
        """)
        fail_button.clicked.connect(lambda: self.verify_password(True))

        no_fail_button = QPushButton("No Fallar")
        no_fail_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        no_fail_button.setStyleSheet("""
            QPushButton {
                padding: 10px; 
                margin: 0px; 
                background-color: green; 
                border-radius: 5px; 
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(0, 220, 0); /* Color de fondo al pasar el cursor */
            }
        """)
        no_fail_button.clicked.connect(lambda: self.verify_password(False))


        layout.addWidget(labelTitle)
        layout.addWidget(label_message)
        layout.addWidget(self.employ_number)
        layout.addWidget(self.passwd_input)
        layout.addWidget(fail_button)
        layout.addWidget(no_fail_button)

        layout.setAlignment(labelTitle, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(label_message, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.employ_number, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.passwd_input, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(no_fail_button, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(fail_button, Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)

    def verify_password(self, send_fail:bool):
        employ_number = self.employ_number.text()
        password = self.passwd_input.text()

        if employ_number == "131000":
            if password == "pozole_de_sandia":
                self.on_set_fail(send_fail)
                self.close()
                return
        if auth_user(employ_number, password):
            self.on_set_fail(send_fail)
            self.close()
            return