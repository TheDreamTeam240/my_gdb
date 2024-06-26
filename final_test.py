import sys
import json
import requests_unixsocket

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QEvent
from PySide6.QtCore import QPoint, QEventLoop, QTimer
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QLabel,
    QListWidget
)
from PySide6.QtGui import QCloseEvent

# class AnotherWindow(QWidget):
#     """
#     This "window" is a QWidget. If it has no parent, it
#     will appear as a free-floating window as we want.
#     """
#     def __init__(self):
#         super().__init__()
#         self.label = QLabel("Window help", self)
#         self.setGeometry(300, 300, 300, 150)

class ExampleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.check = None
        self.isclique = None
        self.function_name = None
        self.bad_file = QLabel(self)
        self.pos_y = 0
        self.index = 0
        self.function = None
        self.new_text = QLabel()
        self.box_layout = QVBoxLayout()
        self.session = requests_unixsocket.Session()
        self.content_widget = QWidget()
        self.function_list = QLabel(WordWrap=True)
        self.list = ["toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon","toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr", "outmomon", "toto", "tata", "tssseeeeeeeeeeeeeerrrrrr",]
        self.edit_text = QLineEdit()
        self.file = self.create_text()
        self.debug_btn = QPushButton(self)
        self.debug_btn.setVisible(False)
        self.debug_box = QDialog()
        self.bp_button = QPushButton(default=False, autoDefault=False)
        self.next_button = QPushButton(default=False, autoDefault=False)
        self.function_bp = None

    def setup(self):
        btn_quit = QPushButton('Force Quit', self)
        self.debug_box = QDialog()
        btn_quit.setStyleSheet("background-color: white; color: black")
        btn_quit.clicked.connect(QApplication.instance().quit)
        btn_quit.resize(btn_quit.sizeHint())
        btn_quit.setFixedWidth(100)
        btn_quit.move(self.screen().size().width() - 150, 50)

        self.setGeometry(100, 100, 200, 150)
        self.setWindowTitle('Window Example')
        self.setStyleSheet("background-color: black; color: white")

        self.file_dialog_button()
        self.help_btn()
        self.title()

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(self, 'Message', 'Voulez vous vraiment quitter?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def file_dialog_button(self):
        file_browser_btn = QPushButton("Choose a binary to analyse", self)
        file_browser_btn.clicked.connect(self.open_file_dialog)
        file_browser_btn.setStyleSheet("background-color: white; color: black")
        file_browser_btn.resize(file_browser_btn.sizeHint())
        file_browser_btn.setFixedWidth(500)
        file_browser_btn.move(self.screen().size().width() / 2 - 500 / 2, self.screen().size().height() - 120)

    def is_bi(self):
        with open(self.filenames[0], 'rb') as f:
            for block in f:
                if b'\0' in block:
                    return True
        return False

    def create_text(self):
        text = QLabel(self)
        font = text.font()
        font.setPointSize(30)
        font.setFamily("Calibri")
        text.move(self.screen().size().width() / 2 - 500 / 2, self.screen().size().height() / 2 - 200)
        text.setFont(font)
        return text

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("All (*)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            self.filenames = dialog.selectedFiles()
            self.path_to_prog = self.filenames[0]
            check = self.is_bi()
            if (check == True):
                if self.filenames:
                    self.file.setText("You chose the " + self.filenames[0].split('/').pop() + " binary")
                    self.file.adjustSize()
                    self.bad_file.setVisible(False)
                    self.file.show()
                    self.cli()
                    self.isvalid = True
            else:
                self.bad_file = QLabel(self)
                self.bad_file = self.create_text()
                self.bad_file.setText("Bad file provided\nPlease chose an ELF file type")
                self.file.setVisible(False)
                self.bad_file.show()
                self.isvalid = False
            if (self.isvalid == True):
                self.debug_button()
            else:
                self.debug_btn.setVisible(False)

    def debug_button(self):
        self.debug_btn = QPushButton("Start debugging the binary", self)
        self.debug_btn.setVisible(True)
        self.debug_btn.setStyleSheet("background-color: white; color: black;")
        self.debug_btn.resize(self.debug_btn.sizeHint())
        self.debug_btn.move(self.screen().size().width() / 2 - 500 / 2, self.screen().size().height() / 2)
        self.debug_btn.setFixedWidth(500)
        self.debug_btn.clicked.connect(self.open_debug)
        self.debug_btn.show()

    def close_debug(self):
        quit = QPushButton("X", self.debug_box, default=False, autoDefault=False)
        quit.setStyleSheet("background-color: white; color: black")
        quit.clicked.connect(self.debug_box.close)
        quit.resize(quit.sizeHint())
        quit.setFixedWidth(20)
        quit.move(self.debug_box.width() - 20, 0)
        quit.show()

    def info_binar(self):
        binary_type = QLabel("Binary type:\nx86-64", self.debug_box)
        binary_type.setStyleSheet("color: red;")
        binary_type.move(self.debug_box.width() - 200, 10)
        binary_type.resize(binary_type.sizeHint())
        font = binary_type.font()
        font.setPointSize(20)
        font.setFamily("Calibri")
        binary_type.setFont(font)
        binary_type.adjustSize()
        binary_type.show()

    def change_color(self):
        self.bp_button.setStyleSheet("background-color: green;")

    def create_break_point(self):
        self.bp_button.setParent(self.debug_box)
        self.bp_button.setText("Set break point to function " + self.function_name)
        self.bp_button.adjustSize()
        self.bp_button.setStyleSheet("background-color: white; color: black")
        self.bp_button.move(self.debug_box.width() / 2, 140)
        self.bp_button.show()

    def stock_function(self):
        self.function_name = self.edit_text.text() # Send to server
        self.set_break_point()
        self.create_break_point()
        self.bp_button.setStyleSheet("background-color: white; color: black")
        self.bp_button.clicked.connect(self.change_color)

    def break_point(self):
        self.edit_text.setParent(self.debug_box)
        self.edit_text.returnPressed.connect(self.stock_function)
        self.edit_text.setStyleSheet("background-color: white; color: black;")
        self.edit_text.move(self.debug_box.width() / 2, 100)
        self.edit_text.setFixedWidth(300)
        self.edit_text.show()

    def title_box(self):
        title_box = QLabel(self.debug_box)
        file = self.filenames[0].split('/').pop()
        title_box.setText("You're actually debugging " + file)
        title_box.setStyleSheet("color: white;")
        font = title_box.font()
        font.setPointSize(20)
        font.setFamily("Calibri")
        title_box.setFont(font)
        title_box.adjustSize()
        title_box.move(self.debug_box.width() / 2 - 150, 30)
        title_box.show()

    def change_text(self):
        self.get_function()
        self.new_text = QLabel(self.scrolli) # get from server
        self.new_text.move(10, self.pos_y)
        self.pos_y += 20
        font = self.new_text.font()
        font.setPointSize(20)
        font.setFamily("Calibri")
        self.new_text.setFont(font)
        self.new_text.setText(self.function)
        if self.function.find("(syscall)") != -1:
            self.new_text.setStyleSheet("color: red")
        else:
            self.new_text.setStyleSheet("color: white")
        self.box_layout.addWidget(self.new_text)
        self.content_widget.setLayout(self.box_layout)
        self.scrolli.setWidget(self.content_widget)
        # self.index += 1
        self.new_text.show()

    def next_function(self):
        self.next_button.setParent(self.debug_box)
        self.next_button.setText("Next function")
        self.next_button.setStyleSheet("background-color: white; color: black")
        self.next_button.adjustSize()
        self.next_button.setStyleSheet("QPushButton { background-color: white }" "QPushButton:pressed { background-color: red }" )
        self.next_button.move(self.debug_box.width() / 2 - 600, self.debug_box.height() / 2 + 300)
        self.next_button.clicked.connect(self.change_text)
        self.next_button.show()

    def function_text(self):
        self.function_list.setParent(self.scrolli)
        self.function_list.setText(self.list[0])
        self.function_list.setStyleSheet("color: white;")
        self.move(50, 50)
        self.function_list.show()

    def ResizeScroll(self, min, maxi):
        self.scrolli.verticalScrollBar().setValue(maxi)

    def display_function(self):
        self.scrolli = QScrollArea(self.debug_box)
        self.scrolli.setStyleSheet("background-color: black;")
        self.scrolli.setWidgetResizable(True)
        bar = self.scrolli.verticalScrollBar()
        bar.rangeChanged.connect( lambda x,y: bar.setValue(y) )
        self.scrolli.move(10, self.debug_box.height() / 2 - 200)
        self.scrolli.setFixedWidth(1400)
        self.scrolli.setFixedHeight(400)
        self.scrolli.adjustSize()
        self.scrolli.verticalScrollBar().setValue(self.scrolli.verticalScrollBar().maximum())
        self.scrolli.show()

    def open_debug(self):
        # self.debug_box = QDialog()
        self.debug_box.setModal(True)
        self.debug_box.setStyleSheet("background-color: black;")
        self.debug_box.setFixedHeight(700)
        self.debug_box.setFixedWidth(1500)
        self.break_point()
        # self.break_pt.activated.connect(self.function_bp_get)
        self.display_function()
        self.change_text()
        self.info_binar()
        self.title_box()
        self.next_function()
        self.close_debug()
        self.debug_box.exec()

    def title(self):
        text_main = QLabel('Ftrace', self)
        font = text_main.font()
        font.setPointSize(40)
        text_main.move(self.screen().size().width() / 2 - 90, 20)
        font.setFamily("Calibri")
        text_main.setFont(font)

    def help_me(self):
        if (self.text_help.isVisible()):
            self.text_help.setVisible(False)
        else:
            self.text_help.setVisible(True)

    def help_btn(self):
        help_button = QPushButton('Help', self)
        help_button.clicked.connect(self.button_clicked)
        help_button.setFixedWidth(100)
        help_button.resize(help_button.sizeHint())
        help_button.move(self.screen().size().width() - 150, self.screen().size().height() - 120)
        help_button.setStyleSheet("background-color: white; color: black;")

    def button_clicked(self):
        dlg = QDialog(self)
        quit = QPushButton('X', dlg)
        help = QLabel("Help window", dlg)
        font = help.font()
        font.setPointSize(20)
        help.move(230, 20)
        font.setFamily("Calibri")
        help.setFont(font)
        quit.setStyleSheet("background-color: white; color: black")
        quit.clicked.connect(dlg.close)
        quit.resize(quit.sizeHint())
        quit.setFixedWidth(20)
        quit.move(580, 0)
        quit.show()
        dlg.setFixedWidth(600)
        dlg.setFixedHeight(500)
        self.text_help = QLabel("Bienvenue sur notre ftrace graphique\nChoissisez un binaire qui vous bloque\net commencer à le debugger grace à notre ftrace\nVous verrez toute les fonctions\nainsi que les syscall appeller par votre binaire", dlg)
        text_help_font = self.text_help.font()
        text_help_font.setPointSize(20)
        text_help_font.setFamily("Calibri")
        self.text_help.move(30, 80)
        self.text_help.setFont(text_help_font)
        dlg.exec()

    def cli(self):
        session = requests_unixsocket.Session()

        response = session.post('http+unix://%2Ftmp%2Fgdb.sock/start',
                                headers={'Content-type':'application/json','Accept':'application/json'},
                                data=json.dumps({'binary_path': self.path_to_prog}))

        # print(response.content)

    def get_function(self):
        response = self.session.get('http+unix://%2Ftmp%2Fgdb.sock/next')
        stock_entire = json.loads(response.content)["name"]
        is_return = json.loads(response.content)["is_return"]
        is_sys = json.loads(response.content)["is_syscall"]
        cut = str(stock_entire)
        stock = cut.split("'")
        if (is_return):
            self.function = stock[1] + " (return)"
        if (is_sys):
            self.function = stock[1] + " (syscall)"

        print(response.content)

    def set_break_point(self):
        response = self.session.post('http+unix://%2Ftmp%2Fgdb.sock/breakpoint',
                                headers={'Content-type':'application/json','Accept':'application/json'},
                                data=json.dumps({'breakpoint': self.function_name}))

        print(self.function_name)

def run():
    app = QApplication(sys.argv)
    ex = ExampleWindow()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    run()