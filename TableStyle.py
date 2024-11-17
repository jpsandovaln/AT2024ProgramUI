#
# @tablestyle.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QHeaderView


class TableStyle(QTableWidget):
    def __init__(self):
        super().__init__()
        self.styleTable()
    #Function to set the table styles
    def styleTable(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectRows)  # Set to select complete rows
        self.setAlternatingRowColors(True)  # Alternative row colours
        self.setStyleSheet("""
                    QTableWidget {
                        background-color: #ffffff;  /* Color de fondo general */
                        alternate-background-color: #e6f2ff;  /* Color de fondo para filas alternas */
                        border: 1px solid #d3d3d3;
                    }
                    QHeaderView::section {
                        background-color: #41689e;  /* Fondo de encabezado */
                        color: white;  /* Color del texto del encabezado */
                        font-weight: bold;
                        padding: 4px;
                        border: 1px solid #d3d3d3;
                    }
                    QTableWidget::item {
                        padding: 8px;  /* Espaciado interno de las celdas */
                        border: 1px solid #d3d3d3;
                    }
                    QTableWidget::item:selected {
                        background-color: #3399ff;  /* Color de fondo para elementos seleccionados */
                        color: white;
                    }
                """)

        # Custom font to cell text
        font = QFont("Arial", 10)
        self.setFont(font)