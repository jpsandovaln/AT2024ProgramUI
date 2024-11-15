from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class HeaderWidget(QWidget):
    def __init__(self, logo_path, app_name="JalaRecognizer"):
        super().__init__()
        self.create_header(logo_path, app_name)
        self.setFixedHeight(80)  # Sets the height of the header

    def create_header(self, logo_path, app_name):
        # Vertical Layout 
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create a widget for the layout
        header_widget = QWidget()
        header_widget.setStyleSheet("background-color: #ffffff;")
        header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Main Horizontal Layout for header
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignVCenter)  # Align elements vertically centered
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Centered Layout for logo and app name
        center_layout = QHBoxLayout()
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(60, 60, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)

        # App name
        colored_name = '<span style="color: #3CB4AC; font-weight: 700;">Jala</span><span style="color: #4FB7E2;">Recognizer</span>'
        name_label = QLabel(colored_name)
        font = QFont("Arial", 22)
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignCenter)

        # Menu Icon
        menu_icon_label = QLabel()
        menu_icon_pixmap = QPixmap('./assets/icons/menu-blue.png')
        if not menu_icon_pixmap.isNull():
            menu_icon_label.setPixmap(menu_icon_pixmap.scaled(35, 35, Qt.KeepAspectRatio))
        menu_icon_label.setAlignment(Qt.AlignRight)
        menu_icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Ensures it maintains its size

        # Add logo and name to center_layout
        center_layout.addWidget(logo_label)
        center_layout.addWidget(name_label)

        # Add center_layout and menu_icon_label to the main header_layout
        header_layout.addLayout(center_layout)   # Centered content
        header_layout.addStretch()               # Spacer to push the menu icon to the right
        header_layout.addWidget(menu_icon_label) # Menu icon aligned to the right

        # Set the layout of header_widget
        header_widget.setLayout(header_layout)

        # Add header_widget into main_layout
        main_layout.addWidget(header_widget)

        # Set main layout into main widget
        self.setLayout(main_layout)
