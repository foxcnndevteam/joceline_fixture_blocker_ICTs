from PyQt5.QtWidgets import QApplication, QWidget
import sys
import typer
import sqlite3

appWindow = QApplication(sys.argv)
window = QWidget()
window.show()  

app = typer.Typer()


if __name__ == "__main__":
    appWindow.exec()