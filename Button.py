import sys
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


class Button(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.set_style()
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def set_style(self):
        self.setStyleSheet("""
                    Button {
                        background-color: #4AD8B5;
                        color: #ffffff;
                        border-radius: 13px;
                        padding: 5px 10px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    Button:hover {
                        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                                            stop:0 rgba(74, 216, 181, 255),
                                            stop:1 rgba(32, 155, 232, 255));
                    }
                """)
