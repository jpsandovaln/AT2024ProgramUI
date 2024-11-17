#
# @imagedialog.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog
from PyQt5.QtGui import  QPixmap
from PyQt5.QtCore import Qt


class ImageDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Imagen Seleccionada")
        self.setGeometry(100, 100, 500, 500)

        # Create a QLabel to show image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Load and show image
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio))

        # Image layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
