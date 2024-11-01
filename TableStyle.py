from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidget, QHeaderView


class TableStyle(QTableWidget):
    def __init__(self):
        super().__init__()
        self.styleTable()
    def styleTable(self):
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectRows)  # Configurar para seleccionar filas completas
        self.setAlternatingRowColors(True)  # Colores alternos en las filas
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

        # Fuente personalizada para el texto de las celdas
        font = QFont("Arial", 10)
        self.setFont(font)