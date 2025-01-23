import sys
import logger
import Utils.lang as lang
import Manager.config as config

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QSizePolicy

class BlockedWindow(QWidget):
    show_fullscreen = True

    def __init__(self, blocked_by: str, show_boards: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupGui(blocked_by, show_boards)
        
    def setupGui(self, blocked_by: str, show_boards: bool):
        try:
            messages = {
                'title': lang.messages['block_view']['title'],
                'subtitle': lang.messages['block_view']['subtitle'],
                'reasons': {
                    f'{blocked_by}': lang.messages['block_view']['reasons'][blocked_by]
                }
            }
        except KeyError as e:
            logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
            sys.exit(0)

        self.setStyleSheet("background-color: #ff4f29;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        labelTitle = QLabel(messages["title"])
        labelTitle.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")


        label = QLabel(messages["subtitle"])
        label.setStyleSheet("font-size: 30px; padding: 0px; margin: 0px; font-weight: bold;")

        labelReason = QLabel("Reason code: " + messages["reasons"][blocked_by])
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

        self.setLayout(layout)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        
    def onJoinPassword(self):
        
        if self.input_text.text() == config.getBlockPassword():
            self.close()
            
    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_Enter or Qt.Key.Key_Return:
            self.onJoinPassword()