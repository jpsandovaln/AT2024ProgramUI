#
# @bluebutton.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import sys
from PyQt5.QtWidgets import QPushButton


class BlueButton(QPushButton):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.set_style()
    #Function to define the style of the button
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
