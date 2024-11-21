from Views.BlockedWindow import BlockedWindow
from Views.RetestWindow import RetestWindow
from PyQt5.QtWidgets import QApplication


class AppView:
    def __init__(self):
        self.app = QApplication([])

    def openBlockedWindow(self, blockedBy: str):
        blockedWindow = BlockedWindow(blockedBy)
        blockedWindow.open()
        self.app.exec()

    def openRetestWindow(self):
        retestWindow = RetestWindow()
        retestWindow.open()
        self.app.exec()