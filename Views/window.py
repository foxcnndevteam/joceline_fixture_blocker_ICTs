import sys

from Views.retest import RetestWindow
from Views.blocked import BlockedWindow
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
windows_to_show: list[QWidget] = []

def openWindows():
    # ow = BlockedWindow("failsLimitReached")
    # ow.showFullScreen()
    
    # ex = RetestWindow()
    # ex.showFullScreen()
    
    for window in windows_to_show:
        if window.show_fullscreen:
            window.showFullScreen()
        else:
            window.show()
    
    if len(windows_to_show) > 0: app.exec_()
    
def show(window: QWidget):
    windows_to_show.append(window)
