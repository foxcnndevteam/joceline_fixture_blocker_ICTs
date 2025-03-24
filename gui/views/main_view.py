from core import config
from Db.Models import Local
from udpsocket import UDPSignals
from core.fixture import get_fixture_yield
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

class MainWindow(QMainWindow):
    def __init__(self, signals: UDPSignals):
        super().__init__()
        
        self.signals = signals
        
        self.setWindowTitle("JDash - ICT")
        # self.setGeometry(100, 100, 800, 500)
        
        self.setFixedSize(800, 500)
        
        self.setup_yield_container()
        self.setup_tests_table()
        self.update_tests_table()
        
        layout = QVBoxLayout()
        layout.addWidget(self.yield_container)
        layout.addWidget(self.table_container)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.signals.update_ui.connect(self.update_ui)
        
    def setup_yield_container(self):
        self.yield_container = QWidget()
        yield_layout = QHBoxLayout(self.yield_container)
        
        self.yield_label = QLabel('Yield:')
        self.yield_label.setStyleSheet("font-size: 30px;")
        
        self.yield_percent = QLabel(f'{int(get_fixture_yield())}%')
        self.yield_percent.setStyleSheet("font-size: 60px; font-weight: bold;")
        
        yield_layout.addWidget(self.yield_label)
        yield_layout.addWidget(self.yield_percent)
        
    def setup_tests_table(self):
        self.table_container = QTableWidget()
        
        self.table_container.setRowCount(config.gey_yield_calc_qty() + 1)
        self.table_container.setColumnCount(7)
        
        self.table_container.horizontalHeader().setStretchLastSection(True) 
        self.table_container.horizontalHeader().setSectionResizeMode( 
            QHeaderView.Stretch
        )
        
        self.table_container.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def update_tests_table(self):
        self.table_container.setItem(0, 0, QTableWidgetItem("Id"))
        self.table_container.setItem(0, 1, QTableWidgetItem("Serial"))
        self.table_container.setItem(0, 2, QTableWidgetItem("Result"))
        self.table_container.setItem(0, 3, QTableWidgetItem("Mode"))
        self.table_container.setItem(0, 4, QTableWidgetItem("Fail status"))
        self.table_container.setItem(0, 5, QTableWidgetItem("Board failed"))
        self.table_container.setItem(0, 6, QTableWidgetItem("Date"))

        tests = self.get_last_tests()

        if tests:
            for i in range(1, ( len(list(tests)) + 1 )):
                self.table_container.setItem(i, 0, QTableWidgetItem(f'{tests[i - 1].id}'))
                self.table_container.setItem(i, 1, QTableWidgetItem(f'{tests[i - 1].serial}'))
                self.table_container.setItem(i, 2, QTableWidgetItem(f'{tests[i - 1].result}'))
                self.table_container.setItem(i, 3, QTableWidgetItem(f'{tests[i - 1].mode}'))
                self.table_container.setItem(i, 4, QTableWidgetItem(f'{tests[i - 1].fail_status}'))
                self.table_container.setItem(i, 5, QTableWidgetItem(f'{tests[i - 1].board_failed}'))
                self.table_container.setItem(i, 6, QTableWidgetItem(f'{tests[i - 1].date}'))
        
    def get_last_tests(self):
        tests = Local.Test().select(
            Local.Test.id,
            Local.Test.serial,
            Local.Test.result,
            Local.Test.fail_status,
            Local.Test.board_failed,
            Local.Test.date,
            Local.Test.mode
        ).limit(config.gey_yield_calc_qty()).order_by(
            Local.Test.date.desc()
        )
        
        return tests
        
    def update_ui(self):
        self.yield_percent.setText(f'{int(get_fixture_yield())}%')
        self.update_tests_table()

    def closeEvent(self, event):
        self.signals.stop_server.set()
        event.accept()