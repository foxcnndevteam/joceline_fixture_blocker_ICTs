from qtwidgets import AnimatedToggle
from gui.assets import get_asset

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QGridLayout, 
)


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
        
        self.config_table.addItem(
            item = ConfigOption(
                option_type = "toggle",
                title_string = "Online mode",
                icon_path = "config_icon.png"
            )
        )
        
        self.config_table.addItem(
            item = ConfigOption(
                option_type = "toggle",
                title_string = "Pausar fallas",
                icon_path = "config_icon.png"
            )
        )
        
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
    
    def __init__(self, option_type: str, title_string: str, icon_path: str):
        super().__init__(None)

        self.option_types = {
            "toggle": self.setup_animated_toggle
        }

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



