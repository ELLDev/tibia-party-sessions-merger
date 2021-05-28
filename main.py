import sys
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)


def format_party_log(input_text):
    list_text = list(input_text.split("\n"))
    formatted_text = []
    players = []
    players_balance = []
    output = ""

    for current_line in list_text:
        if len(current_line) > 0 and "pay" in current_line:
            trim_index = current_line.index("transfer")
            current_line = current_line[trim_index + 9:len(current_line) - 1]
            trim_index = current_line.index("to")
            current_line = current_line[trim_index + 3:] + " " + current_line[:trim_index]
            formatted_text.append(current_line)

    for i in formatted_text:
        for char in i:
            if char.isdigit():
                digit_trim_index = i.index(char)
                break
        j = i[:digit_trim_index - 1]
        i = i[digit_trim_index:]
        players.append(j)
        players_balance.append((j, int(i)))

    my_dict = {key: 0 for key in players}
    for t in players_balance:
        my_dict[t[0]] += t[1]

    for key in my_dict:
        output = output + ("transfer " + str(int(my_dict[key] / 1000) * 1000) + " to " + key + "\n")
    return output


class SessionsMerger(QWidget):
    def __init__(self):
        super(SessionsMerger, self).__init__()

        self.iconName = "icon.ico"
        self.textbox = None
        self.format_button = None
        self.copy_button = None
        self.paste_button = None

        self.setWindowTitle("Party Sessions Merger")
        self.setWindowIcon(QIcon(self.iconName))
        self.setMinimumSize(QSize(880, 680))
        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()
        bottom_buttons_layout = QHBoxLayout()

        self.textbox = QPlainTextEdit(self)
        self.textbox.resize(200, 200)
        outer_layout.addWidget(self.textbox)

        self.format_button = QPushButton(self)
        self.format_button.setText("Merge")
        self.format_button.clicked.connect(self.format_button_handler)
        buttons_layout.addWidget(self.format_button)

        self.paste_button = QPushButton(self)
        self.paste_button.setText("Paste")
        self.paste_button.clicked.connect(self.paste_button_handler)
        bottom_buttons_layout.addWidget(self.paste_button)

        self.copy_button = QPushButton(self)
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(self.copy_button_handler)
        bottom_buttons_layout.addWidget(self.copy_button)

        buttons_layout.addLayout(bottom_buttons_layout)
        outer_layout.addLayout(buttons_layout)
        self.setLayout(outer_layout)

    def format_button_handler(self):
        input_text = self.textbox.toPlainText()
        output_text = format_party_log(input_text)
        self.textbox.setPlainText(output_text)

    def paste_button_handler(self):
        self.textbox.paste()

    def copy_button_handler(self):
        self.textbox.selectAll()
        self.textbox.copy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    mainWin = SessionsMerger()
    mainWin.show()
    sys.exit(app.exec_())
