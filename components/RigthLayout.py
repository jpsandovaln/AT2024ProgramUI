# Rigthlayout.py
from PyQt5.QtWidgets import QVBoxLayout, QTableWidgetItem
from .Button import Button
from PyQt5.QtCore import Qt
from components.TableStyle import TableStyle

class Rigthlayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_rigth()

    def show_rigth(self):
        # Tabla vacia
        self.table = TableStyle()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm", "Word", "Percentage", "Second", "Time"])
        self.addWidget(self.table)

        # Botón inferior de "Show Image"
        self.show_image_button = Button("Show Image")
        self.show_video_point_button = Button("Show in Video")
        self.addWidget(self.show_image_button)
        self.addWidget(self.show_video_point_button)

    def add_new_row(self, data):
        # Insertar una nueva fila al final
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Añadir datos en cada columna de la nueva fila
        for column, item in enumerate(data):

            # Convertir item a str si no es una cadena
            if isinstance(item, (float, int)):  # Si el valor es float o int
                item = str(item)  # Convertirlo a string

            table_item = QTableWidgetItem(item)
            table_item.setTextAlignment(Qt.AlignCenter)  # Centrar el texto en la celda
            table_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # Hacer la celda no editable
            self.table.setItem(row_position, column, table_item)  # Establecer el ítem en la celda
    
    def clear_rows(self):
        self.table.setRowCount(0) 