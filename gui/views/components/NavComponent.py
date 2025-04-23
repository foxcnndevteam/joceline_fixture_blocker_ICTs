from gui.assets import get_asset
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

class NavComponent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            border-radius: 5px;
            background-color: #cccccc;
        """)
        # self.setFixedSize(QSize(50, 50))  # Para que se vea el fondo
        
        self.setup_component()

    def setup_component(self):
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        nav_layout.setContentsMargins(10, 10, 10, 10)

        config_button = QPushButton()
        config_button.setIcon(QIcon(get_asset("icons/config_icon.png")))  # pon tu icono válido
        config_button.setIconSize(QSize(30, 30))
        config_button.setStyleSheet("QPushButton {border: none;}")

        nav_layout.addWidget(config_button)
        self.setLayout(nav_layout)