import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from Utils.MessageLoader import getMessages

import PyQt5

class RetestWindow:

    def __init__(self):
        self.messages = getMessages()

        self.app = QApplication(sys.argv)

        self.window = QWidget()
        self.window.setStyleSheet("background-color: #e5e400;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        labelTitle = QLabel("Favor de colocar la tarjeta en otro equipo")
        labelTitle.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")
        button = QPushButton("Ok")
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setStyleSheet("""
            QPushButton {
                padding: 50px; 
                margin: 0px; 
                background-color: white; 
                border-radius: 5px; 
                text-align: center;
            }
            QPushButton:hover {
                background-color: rgb(220, 220, 220); /* Color de fondo al pasar el cursor */
            }
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.onJoinPassword)
        # button.setFixedHeight(500)
        button.setFixedSize(QSize(200, 500))
        # button.resize(500, 500)

        labelTitle.setFixedHeight(40)
        button.setFixedHeight(30)

        layout.addWidget(labelTitle)
        layout.addWidget(button)

        layout.setAlignment(labelTitle, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignHCenter)

        self.window.setLayout(layout)
        self.window.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.window.showFullScreen()

    def onJoinPassword(self):
        self.app.closeAllWindows()
        # self.app.quit()

    def open(self):
        self.app.exec()
