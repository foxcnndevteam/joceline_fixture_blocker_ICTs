import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
from Utils.MessageLoader import getMessages

class BlockedWindow:

    def __init__(self, blockedBy: str):
        self.messages = getMessages()

        self.app = QApplication(sys.argv)

        self.window = QWidget()
        self.window.setStyleSheet("background-color: #ff4f29;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        labelTitle = QLabel(self.messages["fixture"]["fixBlocked"])
        labelTitle.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")


        label = QLabel(self.messages["fixture"]["blocked"])
        label.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")

        labelReason = QLabel("Reason code: " + self.messages["fixture"][blockedBy])
        labelReason.setStyleSheet("font-size: 20px; padding: 0px; margin: 0px;")

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Password")
        self.input_text.setStyleSheet("padding: 50px; margin: 0px; margin-top: 20px; border: none; border-radius: 5px; background-color: white;")
        self.input_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_text.setEchoMode(QLineEdit.EchoMode.Password)

        button = QPushButton("Continuar")
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
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

        labelTitle.setFixedHeight(40)
        label.setFixedHeight(40)
        labelReason.setFixedHeight(30)
        self.input_text.setFixedHeight(50)
        button.setFixedHeight(30)

        layout.addWidget(labelTitle)
        layout.addWidget(label)
        layout.addWidget(labelReason)
        layout.addWidget(self.input_text)
        layout.addWidget(button)

        layout.setAlignment(labelTitle, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(label, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(labelReason, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(self.input_text, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignHCenter)

        self.window.setLayout(layout)
        self.window.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.window.showFullScreen()

    def onJoinPassword(self):
        if self.input_text.text() == "R!ser2":
            try:
                self.app.closeAllWindows()
            except:
                print("Hubo un error")

    def open(self):
        self.app.exec()
