from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class NavWidget(QWidget):
    right_arrow_clicked = pyqtSignal()
    left_arrow_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.create_nav_area()

    def create_nav_area(self):
        # Vertical Layout (main container)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create a widget for the layout
        nav_widget = QWidget()
        nav_widget.setStyleSheet("background-color: #41689E;")
        nav_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Horizontal Layout for Navigation Tab
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)
        nav_layout.setSpacing(10)

        # Reusable method to create arrow labels
        def create_arrow_label(image_path, size=(30, 30)):
            label = QLabel()
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                label.setPixmap(pixmap.scaled(*size, Qt.KeepAspectRatio))  
            label.setAlignment(Qt.AlignCenter)
            return label
        
        # Left Arrow (aligned to the left)
        self.left_arrow_label = create_arrow_label('./assets/icons/left-arrow-white.png')

        # App name (centered)
        feature_name = '<span style="color: #ffffff;">Video Frame Analyzer</span>'
        self.name_label = QLabel(feature_name)
        font = QFont("Arial", 12, QFont.Bold)  
        self.name_label.setFont(font)
        self.name_label.setAlignment(Qt.AlignCenter)

        # Right Arrow (aligned to the right)
        self.right_arrow_label = create_arrow_label('./assets/icons/right-arrow-white.png')

        # Conectar el clic en el right_arrow_label con la señal
        self.left_arrow_label.mousePressEvent = self.on_left_arrow_click
        self.right_arrow_label.mousePressEvent = self.on_right_arrow_click

        # Add widgets to nav_layout
        nav_layout.addWidget(self.left_arrow_label)
        nav_layout.addStretch(1)  # Stretch to push left_arrow to the left
        nav_layout.addWidget(self.name_label)
        nav_layout.addStretch(1)  # Stretch to center the name_label
        nav_layout.addWidget(self.right_arrow_label)

        # Set the layout of nav_widget
        nav_widget.setLayout(nav_layout)

        # Add nav_widget to the main layout
        main_layout.addWidget(nav_widget)

        # Set the main layout for this widget
        self.setLayout(main_layout)

    def on_right_arrow_click(self, event):
        # Emitir la señal cuando se hace clic en el right_arrow_label
        self.right_arrow_clicked.emit()

    def on_left_arrow_click(self, event):
        # Emitir la señal cuando se hace clic en el right_arrow_label
        self.left_arrow_clicked.emit()
    
    def update_feature_name(self, new_name):
        # Método para actualizar el nombre de la función
        self.name_label.setText(f'<span style="color: #ffffff;">{new_name}</span>')