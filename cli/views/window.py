import sys
from cli.views.failauthorization import FailAuthorizationWindow
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
# ~ List of windows instances to show
windows_to_show: list[QWidget] = []


'''
#   Function: openWindows
#   Desc: Iterate in windows to show list, check if should be diplayed in full screen and show it.
'''
def openWindows():
    for window in windows_to_show:
        if window.show_fullscreen:
            window.showFullScreen()
        else:
            window.show()
    
    # ~ If is one or more window instances in list, execute app.
    if len(windows_to_show) > 0: app.exec_()

def openWindowAuth(on_set_fail, message = ""):
    win = FailAuthorizationWindow(on_set_fail, message)
    win.showFullScreen()
    app.exec_()

'''
#   Function: show
#   Desc: Add an window instance to list
#   Arguments:
#       window | type:QWidget  | Window instance
'''
def show(window: QWidget):
    windows_to_show.insert(0, window)
