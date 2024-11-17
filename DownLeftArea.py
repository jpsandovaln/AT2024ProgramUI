#
# @downleftarea.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit,        QListWidget
from BlueButton import BlueButton


class DownLeftArea(QWidget):
    def __init__(self):
        super().__init__()
        self.create_down_left_area()
    #Function to set the structure of the down left area
    def create_down_left_area(self):
        down_left_layout = QVBoxLayout()
        
        # Add image upload section
        image_path_label = QLabel('Provide image for comparison:\n(Only works with Face Recognizer)')
        self.image_path_input = QLineEdit()
        self.image_path_input.setReadOnly(True)  # It  doesn't allow to edit
        self.browse_image_button = BlueButton('Browse Image')
        self.browse_image_button.setEnabled(False)  # Initially disabled
        
        # Adding widgets to layout
        down_left_layout.addWidget(image_path_label)
        down_left_layout.addWidget(self.image_path_input)
        down_left_layout.addWidget(self.browse_image_button)
        
        self.setLayout(down_left_layout)

    # Setter of the model
    def set_model(self, model_name):
            self.browse_image_button.setEnabled(model_name == 'Face Recognizer')

    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
        
