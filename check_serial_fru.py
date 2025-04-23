import os
import re
import sys

from env import BASE_DIR

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout,QSizePolicy
from PyQt5.QtWidgets import QApplication, QWidget

# --- Var options will be added in program config --- #
header_len = 2
hex_dump_line_len = 57
scanned_sn_regex = r'Serial\s*:\s*(.*)'
    
sn_men_add_start = 2
sn_mem_add_end = 3

fru_output_filename = "fru_output"
# --------------------------------------------------- #

def get_scanned_sn(data: str):
    return re.search( scanned_sn_regex, data )[1]

def get_fru_sn(data: str):
    split_data = list(
        data.split('\n')
    )
    
    fru_log_data = split_data[header_len::]

    return ''.join(
        hex_dump_line[hex_dump_line_len + 1:]
        for hex_dump_line in fru_log_data[sn_men_add_start:sn_mem_add_end + 1]
    )

def save_retest_result_in_path(result: str):
    result_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(result_path): os.makedirs(result_path)
    
    with open(os.path.join(result_path, "should_retest") + "", "w") as f:
        f.write(result)

def should_burn_fru_twice():
    with open(os.path.join(BASE_DIR, fru_output_filename), "r+") as file:
        data = file.read()
        
        scanned_sn = get_scanned_sn(data)
        fru_sn = get_fru_sn(data)
        
        if scanned_sn in fru_sn:
            return False
        else:
            save_retest_result_in_path("True")
                        
            show(RetestWindow([], invalid_fru=True))
            openWindows()
            return True


'''
#   Class: RetestWindow
#   Desc: This is the retest window wich is diplayed when board/s should be retested
'''
class RetestWindow(QWidget):
    # ~ Used in all windows instance on cli to check if cli should display it in full screen
    show_fullscreen = True


    '''
    #   Function: __init__        -        Class instance
    #   Arguments:
    #       boards_to_retest | type:list[str]  | List to check if arr position in boards should retest
    '''
    def __init__(self, boards_to_retest:list[str], invalid_fru: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupGui(boards_to_retest, invalid_fru)


    '''
    #   Function: setupGui
    #   Desc: Instance initial GUI componentes
    #   Arguments:
    #       boards_to_retest | type:list[str]  | List to check if arr position in boards should retest
    '''
    def setupGui(self, boards_to_retest:list[str], invalid_fru: bool):
        
        title = "La tarjeta tiene un serial en FRU invalido"
        view_background = '#CD7F32'

        self.setStyleSheet(f'background-color: {view_background};')

        layout = QVBoxLayout()

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
        button.clicked.connect(self.onPress)
        button.setFixedSize(QSize(200, 500))

        labelTitle.setFixedHeight(40)
        button.setFixedHeight(30)

        layout.addWidget(labelTitle)
        layout.addWidget(button)

        layout.setAlignment(labelTitle, Qt.AlignmentFlag.AlignHCenter)
        layout.setAlignment(button, Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)


    '''
    #   Function: onPress
    #   Desc: Function called when press event that close window
    '''
    def onPress(self):
        self.close()
    
    
    '''
    #   Function: keyPressEvent
    #   Desc: Detect if enter is clicked to auto send form
    #   Arguments:
    #       e | type:QKeyEvent  | Argument to get key event
    '''
    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key.Key_Enter or Qt.Key.Key_Return:
                self.onPress()



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


'''
#   Function: show
#   Desc: Add an window instance to list
#   Arguments:
#       window | type:QWidget  | Window instance
'''
def show(window: QWidget):
    windows_to_show.insert(0, window)
    
    
    
    






if __name__ == "__main__":
    print(should_burn_fru_twice())