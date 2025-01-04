import os
import sys
import json
import logger
import Utils.lang as lang

from env import BASE_DIR

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy, QGridLayout


class RetestWindow:

    def __init__(self, show_boards):
        try:
            messages = {
                "show_boards_title": lang.messages["retest_view"]["show_boards_title"],
                "default_title": lang.messages["retest_view"]["default_title"],
            }
        except KeyError as e:
            logger.error(f'Corrupted lang file: Missing key "{e.args[0]}" in lang file')
            sys.exit(0)

        boards_to_retest = self.getBoards()

        if len(boards_to_retest) == 0 and show_boards: sys.exit(0)

        if show_boards:
            view_background = 'rgb(240, 240, 240)'
            title = messages["show_boards_title"]
        else:
            view_background = '#e5e400'
            title = messages["default_title"]

        self.app = QApplication(sys.argv)

        self.window = QWidget()
        self.window.setStyleSheet(f'background-color: {view_background};')

        layout = QVBoxLayout()

        if show_boards:
            fixture_layout = QGridLayout()
            fixture_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            labels_texts = ["1", "2", "3", "4"]
            labels_positions = [(0, 0), (1, 0), (0, 1), (1, 1)]

            for text, position in zip(labels_texts, labels_positions):
                label = QLabel(text)
                style = """
                    font-size: 30px;
                    border: 1px solid black;
                """
                if int(text) in boards_to_retest: style = style + "background-color: #e5e400;"

                label.setStyleSheet(style)
                label.setFixedWidth(300)
                label.setFixedHeight(150)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                

                fixture_layout.addWidget(label, position[0], position[1])

        labelTitle = QLabel(title)
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
                background-color: rgb(220, 220, 220); 
            }
        """)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(self.onJoinPassword)
        button.setFixedSize(QSize(200, 500))

        labelTitle.setFixedHeight(40)
        button.setFixedHeight(30)

        layout.addWidget(labelTitle)
        if show_boards: layout.addLayout(fixture_layout)
        layout.addWidget(button)

        layout.setAlignment(labelTitle, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignHCenter)

        self.window.setLayout(layout)
        self.window.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.window.showFullScreen()

    def getBoards(self):
        boards_filename = "boards_to_retest.json"
        boards_path = os.path.join(BASE_DIR, boards_filename)

        if not os.path.isfile(boards_path): return []

        with open(boards_path, 'r+') as file:
            boards = json.loads(file.read())

        with open(boards_path, 'w') as file:
            file.write("[]")
        
        return boards

    def onJoinPassword(self):
        self.app.closeAllWindows()

    def open(self):
        self.app.exec()
