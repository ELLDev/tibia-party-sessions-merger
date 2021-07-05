import sys
from tibiapal_logs_merger import merge_tibiapal_lootsplit_logs
from raw_session_merger import merge_raw_session_logs
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QPlainTextEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QApplication,
    QTabWidget,
)


class SessionsMerger(QWidget):
    def __init__(self):
        super(SessionsMerger, self).__init__()

        self.iconName = "../img/icon.ico"
        self.raw_sessions_textbox = None
        self.tibiapal_logs_textbox = None
        self.merge_button = None

        self.setWindowTitle("Party Sessions Merger")
        self.setWindowIcon(QIcon(self.iconName))
        self.setMinimumSize(QSize(880, 680))

        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.addTab(self.raw_sessions_tab_ui(), "Raw Party Sessions")
        tabs.addTab(self.tibiapal_logs_tab_ui(), "TibiaPal LootSplit Logs")
        layout.addWidget(tabs)
        self.setLayout(layout)

    def raw_sessions_tab_ui(self):
        raw_sessions_tab = QWidget()

        outer_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()

        self.raw_sessions_textbox = QPlainTextEdit(self)
        outer_layout.addWidget(self.raw_sessions_textbox)

        self.merge_button = QPushButton(self)
        self.merge_button.setText("Merge")
        self.merge_button.clicked.connect(self.merge_button_handler)
        buttons_layout.addWidget(self.merge_button)

        outer_layout.addLayout(buttons_layout)
        self.setLayout(outer_layout)
        raw_sessions_tab.setLayout(outer_layout)

        return raw_sessions_tab

    def tibiapal_logs_tab_ui(self):
        tibiapal_logs_tab = QWidget()

        outer_layout = QVBoxLayout()
        buttons_layout = QVBoxLayout()

        self.tibiapal_logs_textbox = QPlainTextEdit(self)
        outer_layout.addWidget(self.tibiapal_logs_textbox)

        self.merge_button = QPushButton(self)
        self.merge_button.setText("Merge")
        self.merge_button.clicked.connect(self.tibiapal_merge_button_handler)
        buttons_layout.addWidget(self.merge_button)

        outer_layout.addLayout(buttons_layout)
        self.setLayout(outer_layout)
        tibiapal_logs_tab.setLayout(outer_layout)

        return tibiapal_logs_tab

    def merge_button_handler(self):
        input_text = self.raw_sessions_textbox.toPlainText()
        output_text = merge_raw_session_logs(input_text)
        self.raw_sessions_textbox.setPlainText(output_text)

    def tibiapal_merge_button_handler(self):
        input_text = self.tibiapal_logs_textbox.toPlainText()
        output_text = merge_tibiapal_lootsplit_logs(input_text)
        self.tibiapal_logs_textbox.setPlainText(output_text)


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
    window = SessionsMerger()
    window.show()
    sys.exit(app.exec_())
