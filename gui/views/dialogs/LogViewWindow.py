import os
from env import BASE_DIR
from PyQt5.QtWidgets import ( QDialog, QVBoxLayout, QTextEdit )

class LogDialog(QDialog):

  def __init__(self, log_name: str = ''):
    super().__init__()
    self.setWindowTitle(f'log:{log_name}')
    self.setFixedSize(580, 380)

    # setup    
    layout = QVBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    log_info = QTextEdit()
    log_info.setDisabled(True)

    # loading log

    log_path = os.path.join(BASE_DIR,'reports',log_name)

    if os.path.exists(log_path):
      with open(log_path, 'r') as logf:
        content = logf.read()
        log_info.setText(content)
    else:
      log_info.setText('log no encotrado')

    # init
    layout.addWidget(log_info)
    self.setLayout(layout)
