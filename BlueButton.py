import sys
from PyQt5.QtWidgets import QPushButton


class BlueButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.set_style()

    def set_style(self):
        self.setStyleSheet("""
                    BlueButton {
                        background-color: #41689e;
                        color: #ffffff;
                        border-radius: 1px;
                        padding: 5px 10px;
                        font-size: 14px;
                    }
                    BlueButton:hover {
                        background-color: #0056b3;
                    }
                """)
