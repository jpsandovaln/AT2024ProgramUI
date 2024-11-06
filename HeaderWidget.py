from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class HeaderWidget(QWidget):
    def __init__(self, logo_path, app_name="JalaRecognizer"):
        super().__init__()
        self.create_header(logo_path, app_name)
        #self.setStyleSheet("background-color: red; color: white;")
        self.setFixedHeight(60) # Set a fixed height for the header to prevent expansion

    def create_header(self, logo_path, app_name):
        # Crea layout horizontal para el header
        header_layout = QHBoxLayout()
        
        # Reduce padding by setting smaller margins
        header_layout.setContentsMargins(80, 0, 5, 0)  # Adjust these values as needed
        header_layout.setSpacing(380)  # Adjust spacing between logo and text

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio))  
        logo_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Nombre de la aplicacion
        name_label = QLabel(app_name)
        font = QFont("Arial", 18, QFont.Bold)
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Agregar logo y nombre a layout de header
        header_layout.addWidget(logo_label)
        header_layout.addWidget(name_label)
        header_layout.addStretch()  # Empuja contenido a la izquierda
        
        # Agregando layout all widget widget
        self.setLayout(header_layout)
