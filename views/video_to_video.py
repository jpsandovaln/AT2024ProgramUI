import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea import UpperLeftArea
from components.DownLeftArea import DownLeftArea
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from SaveFile import SaveFile
from ImageDialog import ImageDialog
import requests
import json
import zipfile


class VideoToVideoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        # Window configurations
        self.setWindowTitle('JalaRecognizer')
        self.setGeometry(100, 100, 1000, 700)

        # General Layout
        overall_layout = QVBoxLayout()
        overall_layout.setContentsMargins(0, 0, 0, 10)
        overall_layout.setSpacing(0)

        # Header widget in the top side
        header_widget = HeaderWidget("./assets/img/logo.png")
        overall_layout.addWidget(header_widget)

        # Nav layout under Header
        self.nav_widget = NavWidget()
        overall_layout.addWidget(self.nav_widget)

        # Conectar la señal del right_arrow_clicked con el método de apertura de una nueva ventana
        self.nav_widget.left_arrow_clicked.connect(self.open_left_window)
        self.nav_widget.right_arrow_clicked.connect(self.open_left_window)

        self.update_function_name('Video to Video Convertor')

        # Main Horizontal Layout 
        main_layout = QHBoxLayout()

        # Main left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)
        
        # Left area of labels and buttons
        self.upper_left_area = UpperLeftArea()
        
        # Add areas into left layout
        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Crear una instancia de CenterLayout
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your video and select the object, face, or person (male or female) you want to search for. Using Machine Learning, the system analyzes each frame of the video and provides a list of results where the selected object, face, or person is detected, helping you find exactly what you're looking for in the video."
        )

        # Initially hide right_layout and show center_widget
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)  # Asignar el layout a un widget contenedor
        self.right_widget.hide()  # Inicialmente ocultamos el RightLayout

        # Add the layouts into the main layout
        main_layout.addLayout(left_layout, 1)  #  1 is the expansion factor 
        main_layout.addWidget(self.center_widget, 3, alignment=Qt.AlignCenter)  # 3 is the expansion factor for the center_widget
        main_layout.addWidget(self.right_widget, 3) 
        # Add main_layout into overall_layout
        overall_layout.addLayout(main_layout)

        # Add overall layout into window
        self.setLayout(overall_layout)

    def open_left_window(self):
        # Importar MainWindow solo cuando sea necesario
        from main import MainWindow

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = MainWindow()
        self.new_window.show()
    
    def update_function_name(self, new_name):
        # Llamar al método del NavWidget para actualizar el nombre
        self.nav_widget.update_feature_name(new_name)