from typing import Literal
from qtwidgets import AnimatedToggle
from gui.assets import get_asset

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QGridLayout, 
    QComboBox
)
from core.config import get_online_mode, get_pause_on_fail, set_online_mode, set_pause_on_fail, get_rma_mode, set_rma_mode
from core.fixture import save_should_pause_in_path

def set_shloud_pause(pause_on_fail:bool):
    set_pause_on_fail(pause_on_fail)
    save_should_pause_in_path()

class ConfigPanel(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_config_table()
        
        layout = QVBoxLayout(self)
        
        layout.addWidget(self.config_table)
   
    def setup_config_table(self):
        self.config_table = FlowPanel(
            parent = self, 
            grid_columns = 5
        )
        
        # self.config_table.addItem(
        #     item = ConfigOption(
        #         option_type = "toggle",
        #         title_string = "Online mode",
        #         icon_path = "config_icon.png",
        #         getter=get_online_mode,
        #         setter=set_online_mode
        #     )
        # )
        
        # self.config_table.addItem(
        #     item = ConfigOption(
        #         option_type = "toggle",
        #         title_string = "Pausar fallas",
        #         icon_path = "config_icon.png",
        #         getter=get_pause_on_fail,
        #         setter=set_shloud_pause
        #     )
        # )

        # self.config_table.addItem(
        #     item = ConfigOption(
        #         option_type="toggle",
        #         title_string="Modo RMA",
        #         icon_path= "rma_mode.png",
        #         getter=get_rma_mode,
        #         setter=set_rma_mode
        #     )
        # )

        self.config_table.addItem(item=ModeOption())

        
class FlowPanel(QWidget):
    
    def __init__(self, parent = None, grid_columns: int = 5):
        super().__init__(parent)
        self.current_column = 0
        self.grid_columns = grid_columns

        self.setContentsMargins(0, 0, 0, 0)

        self.table_layout = QGridLayout(self)
        

    def addItem(self, item):
        row = self.current_column // self.grid_columns
        col = self.current_column % self.grid_columns
        self.table_layout.addWidget(item, row, col)
        
        self.current_column += 1
        
class ConfigOption(QWidget):
    
    def __init__(self, option_type: str, title_string: str, icon_path: str, getter, setter):
        super().__init__(None)

        self.option_types = {
            "toggle": self.setup_animated_toggle
        }

        self.getter = getter
        self.setter = setter

        self.setObjectName("Option")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMaximumSize(QSize(250, 250))
        self.setStyleSheet("""
            #Option {
                background-color: #dfdfdf;
                border-radius: 5px;
            }
        """)
        
        self.setup_icon(icon_path)
        self.setup_title(title_string)
        self.setup_input_type(option_type)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.icon_widget)
        layout.addWidget(self.title_widget)
        layout.addWidget(self.input_widget)
    
    def setup_input_type(self, option_type: str):
        input_func = self.option_types[option_type]
        self.input_widget = input_func()
    
    def setup_animated_toggle(self):
        animated_toggle = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        animated_toggle.setMinimumHeight(70)
        animated_toggle.setStyleSheet("""
            border: 1px solid black;
        """)
        def msg(estado):
            self.setter(estado == 2)
        animated_toggle.stateChanged.connect(msg)
        animated_toggle.setChecked(self.getter())
        return animated_toggle
        
    def setup_title(self, tilte_string: str):
        self.title_widget = QLabel(tilte_string)
        self.title_widget.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.title_widget.setStyleSheet("""
             font-size: 20px;
            font-weight: bold;
        """)
    
    def setup_icon(self, icon_path):
        icon_map = QPixmap(get_asset(f"icons/{icon_path}"))
        self.icon_widget = QLabel(self)
        self.icon_widget.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.icon_widget.setPixmap(icon_map)
        
        # self.icon_widget.resize(
            # 50,
            # 50
        # )


class ModeOption(QWidget):
    def __init__(self):
        super().__init__(None)

        self.setObjectName("Option")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMaximumSize(QSize(440, 200))
        self.setStyleSheet("""
            #Option {
                background-color: #dfdfdf;
                border-radius: 5px;
            }
        """)

        self.setup_title('Operation Mode')
        self.setup_select_box()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title_widget)
        layout.addWidget(self.combobox)



    def setup_title(self, tilte_string: str):
        self.title_widget = QLabel(tilte_string)
        self.title_widget.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.title_widget.setStyleSheet("""
             font-size: 40px;
            font-weight: bold;
        """)


    def __get_mode(self) -> Literal['Online', 'Offline', 'RMA']:
        if get_rma_mode():
            return 'RMA'
        
        if get_online_mode():
            return 'Online'

        return 'Offline'
    
    def __set_mode(self, _):
        selected_option = self.combobox.currentText()
        
        match selected_option:
            case 'Online':
                set_online_mode(True)
                set_rma_mode(False)
                set_pause_on_fail(False)
            case 'Offline':
                set_online_mode(False)
                set_rma_mode(False)
                set_pause_on_fail(True)
            case 'RMA':
                set_rma_mode(True)
                set_pause_on_fail(True)

    def setup_select_box(self):
        self.combobox = QComboBox()
        self.combobox.addItems(['Online', 'Offline', 'RMA'])
        self.combobox.setCurrentText(self.__get_mode())
        self.combobox.activated.connect(self.__set_mode)
        self.combobox.setObjectName('combobox')
        self.combobox.setStyleSheet("""
            #combobox {
                font-size: 37px;
                padding: 5px;
                border-radius: 8px;
                }
            """)

