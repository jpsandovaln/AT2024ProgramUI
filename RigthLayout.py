#
# @rigthlayout.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from BlueButton import BlueButton
from PyQt5.QtCore import Qt

from TableStyle import TableStyle


class Rigthlayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_rigth()
    #Set the structure of the table
    def show_rigth(self):
        # Tabla vacia
        self.table = TableStyle()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm", "Word", "Percentage", "Second", "Time"])
        self.addWidget(self.table)

        # Lower "Show Image" button
        self.show_image_button = BlueButton("Show Image")
        self.addWidget(self.show_image_button)
    #Function to add a new row in the table
    def add_new_row(self, data):
        # Insert new row at the end
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Add data in each column of new row
        for column, item in enumerate(data):
            table_item = QTableWidgetItem(item)
            table_item.setTextAlignment(Qt.AlignCenter)  # Centrar el texto en la celda
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Hacer la celda no editable
            self.table.setItem(row_position, column, table_item)
            #self.table.setItem(row_position, column, QTableWidgetItem(item))