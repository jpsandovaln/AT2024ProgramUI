from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class HeaderWidget(QWidget):
    def __init__(self, logo_path, app_name="JalaRecognizer"):
        super().__init__()
        self.create_header(logo_path, app_name)
        self.setFixedHeight(50)  # Sets the height of the header

    def create_header(self, logo_path, app_name):
        # Vertical Layout 
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Horizontal Layout for logo and app name
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(0)  # Space between logo and app name

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(90, 90, Qt.KeepAspectRatio))  
        logo_label.setAlignment(Qt.AlignCenter)

        # App name
        colored_name = '<span style="color: #3CB4AC;">Jala</span><span style="color: #4FB7E2;">Recognizer</span>'
        name_label = QLabel(colored_name)
        font = QFont("Arial", 22, QFont.Bold)  
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignCenter)

        # Add widgets to header_layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(name_label)

        # Add header layout into main_layout
        main_layout.addLayout(header_layout)

        # Set main layout into main widget
        self.setLayout(main_layout)
