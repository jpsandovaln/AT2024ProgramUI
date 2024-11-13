from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit,        QListWidget
from components.Button import Button


class DownLeftArea(QWidget):
    def __init__(self):
        super().__init__()
        self.create_down_left_area()

    def create_down_left_area(self):
        down_left_layout = QVBoxLayout()
        
        # Add image upload section
        image_path_label = QLabel('Provide image for comparison:\n(Only works with Face Recognizer)')
        self.image_path_input = QLineEdit()
        self.image_path_input.setReadOnly(True)  # It  doesn't allow to edit
        self.browse_image_button = Button('Browse Image')
        self.browse_image_button.setEnabled(False)  # Initially disabled
        
        # Adding widgets to layout
        down_left_layout.addWidget(image_path_label)
        down_left_layout.addWidget(self.image_path_input)
        down_left_layout.addWidget(self.browse_image_button)
        
        self.setLayout(down_left_layout)

    def set_model(self, model_name):
            self.browse_image_button.setEnabled(model_name == 'Face Recognizer')

    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
        
