from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from BlueButton import BlueButton


class Rigthlayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.show_rigth()
        self.styleTable()

    def show_rigth(self):
        # Tabla vacia
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Algorithm", "Word", "Percentage", "Second", "Time"])
        self.addWidget(self.table)

        # Botón inferior de "Show Image"
        self.show_image_button = BlueButton("Show Image")
        self.addWidget(self.show_image_button)


    def add_new_row(self, data):
        # Insertar una nueva fila al final
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Añadir datos en cada columna de la nueva fila
        for column, item in enumerate(data):
            self.table.setItem(row_position, column, QTableWidgetItem(item))

    def styleTable(self):
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)  # Colores alternos en las filas
        self.table.setStyleSheet("""
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

        # Fuente personalizada para el texto de las celdas
        font = QFont("Arial", 10)
        self.table.setFont(font)
