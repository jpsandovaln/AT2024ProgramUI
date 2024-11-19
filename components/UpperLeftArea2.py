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
        self.browse_button = Button('Browse')
        self.outputformat_label = QLabel('Format to convert:')
        self.outputformat_input = QComboBox()
        self.fps_label = QLabel('FPS:')
        self.fps_input = QLineEdit()
        self.vcodec_label = QLabel('Vcodec:')
        self.vcodec_input = QComboBox()
        self.acodec_label = QLabel('Acodec:')
        self.acodec_input = QComboBox()
        self.achannel_label = QLabel('Audio Channels:')
        self.achannel_input = QComboBox()

        self.search_button = SearchButton('Convert')

        # Add to the upper left layout
        upper_left_layout.addWidget(video_path_label)
        upper_left_layout.addWidget(self.video_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(self.outputformat_label)
        upper_left_layout.addWidget(self.outputformat_input)
        upper_left_layout.addWidget(self.fps_label)
        upper_left_layout.addWidget(self.fps_input)
        upper_left_layout.addWidget(self.vcodec_label)
        upper_left_layout.addWidget(self.vcodec_input)
        upper_left_layout.addWidget(self.acodec_label)
        upper_left_layout.addWidget(self.acodec_input)
        upper_left_layout.addWidget(self.achannel_label)
        upper_left_layout.addWidget(self.achannel_input)
        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

        self.update_comboBoxes()
    
    def update_comboBoxes(self):
        self.outputformat_input.clear()
        self.fps_input.clear()
        self.vcodec_input.clear()
        self.acodec_input.clear()
        self.achannel_input.clear()
        with open('data/videoFormatOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.outputformat_input.addItems(words)
        with open('data/vcodecOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.vcodec_input.addItems(words)
        with open('data/acodecOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.acodec_input.addItems(words)
        with open('data/audioChannelsOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.achannel_input.addItems(words)

    # Getters
    def get_video_path(self):
        return self.video_path_input.text()

    def get_word(self):
        return self.word_input.currentText()

    def get_percentage_label(self):
        return self.percentage_combobox.currentText()
    
    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
