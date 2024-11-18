from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox, QPushButton
from .Button import Button, SearchButton


class UpperLeftArea2(QWidget):
    def __init__(self):
        # Constructor inherits and creates upper left area
        super().__init__()
        self.create_upper_left_area()

    def create_upper_left_area(self):
        upper_left_layout = QVBoxLayout()

        # Creating labels , inputs and buttons
        video_path_label = QLabel('Video Path:')
        self.video_path_input = QLineEdit()
        self.video_path_input.setReadOnly(True)
        self.browse_button = Button('Browse Image')
        self.outputformat_label = QLabel('Format to convert:')
        self.outputformat_path_input = QLineEdit()

        self.search_button = SearchButton('Search')

        # Add to the upper left layout
        upper_left_layout.addWidget(video_path_label)
        upper_left_layout.addWidget(self.video_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(self.outputformat_label)
        upper_left_layout.addWidget(self.outputformat_path_input)
        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

    # Getters
    def get_video_path(self):
        return self.video_path_input.text()

    def get_word(self):
        return self.word_input.currentText()

    def get_neural_network_model(self):
        return self.neural_network_model_combobox.currentText()

    def get_percentage_label(self):
        return self.percentage_combobox.currentText()
    
    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
