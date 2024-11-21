# components/CenterLayout.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CenterLayout(QWidget):
    def __init__(self, image_path: str, label_text: str, parent=None):
        super().__init__(parent)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes
        layout.setSpacing(10)  # Espacio entre widgets

        # Imagen
        image_label = QLabel()
        image_pixmap = QPixmap(image_path)
        if not image_pixmap.isNull():
            image_label.setPixmap(image_pixmap.scaled(180, 180, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(180)

        # Texto (almacena la referencia)
        self.frame_label = QLabel(label_text)  # Cambiar aquí
        self.frame_label.setAlignment(Qt.AlignCenter)
        self.frame_label.setWordWrap(True)
        self.frame_label.setStyleSheet("font-size: 16px;")
        self.frame_label.setFixedWidth(550)

        # Añadir widgets al layout
        layout.addWidget(image_label)
        layout.addWidget(self.frame_label)  # Usar la referencia

        # Establecer layout en el widget
        self.setLayout(layout)

        # Asegurarse de que los cambios se apliquen correctamente
        self.updateGeometry()

    def change_label_text(self, label):
        self.frame_label.setText(label)  # Actualiza directamente el texto
