import sys

from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
windows_to_show: list[QWidget] = []

def openWindows():
    for window in windows_to_show:
        if window.show_fullscreen:
            window.showFullScreen()
        else:
            window.show()
    
    if len(windows_to_show) > 0: app.exec_()
    
def show(window: QWidget):
    windows_to_show.insert(0, window)
