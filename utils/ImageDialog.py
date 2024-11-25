from PyQt5.QtWidgets import QVBoxLayout, QLabel, QDialog
from PyQt5.QtGui import  QPixmap
from PyQt5.QtCore import Qt


class ImageDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Imagen Seleccionada")
        self.setGeometry(100, 100, 500, 500)

        # Crear un QLabel para mostrar la imagen
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Cargar y mostrar la imagen
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio))

        # Layout para la imagen
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
