##
## EPITECH PROJECT, 2023
## my_gdb
## File description:
## __main__.py
##

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

def main(args: list[str]) -> int:
    qml = ""
    with open("qml/main.qml", "r") as file:
        qml = file.read()

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.loadData(qml.encode('utf-8'))

    if not engine.rootObjects():
        return 84
    
    exit_code = app.exec()
    del engine

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
