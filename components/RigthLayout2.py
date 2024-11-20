# Rigthlayout.py
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from .Button import Button
from PyQt5.QtCore import Qt
from components.TableStyle import TableStyle

class Rigthlayout2(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_rigth()

    def show_rigth(self):
        # Tabla vacia
        self.table = TableStyle()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Data", "Value"])
        self.addWidget(self.table)

    def add_new_row(self, data):
        # Insertar una nueva fila al final
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Añadir datos en cada columna de la nueva fila
        for column, item in enumerate(data):

            table_item = QTableWidgetItem(item)
            table_item.setTextAlignment(Qt.AlignLeft)  # Centrar el texto en la celda
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Hacer la celda no editable
            self.table.setItem(row_position, column, table_item)  # Establecer el ítem en la celda
    
    def clear_rows(self):
        self.table.setRowCount(0) 