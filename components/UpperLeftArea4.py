from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox, QPushButton
from .Button import Button, SearchButton


class UpperLeftArea4(QWidget):
    def __init__(self):
        # Constructor inherits and creates upper left area
        super().__init__()
        self.create_upper_left_area()

    def create_upper_left_area(self):
        upper_left_layout = QVBoxLayout()

        # Creating labels , inputs and buttons
        audio_path_label = QLabel('Audio Path:')
        self.audio_path_input = QLineEdit()
        self.audio_path_input.setReadOnly(True)
        self.browse_button = Button('Browse')
        self.outputformat_label = QLabel('Format to convert:')
        self.outputformat_input = QComboBox()
        self.bitrate_label = QLabel('Bit rate:')
        self.bitrate_input = QComboBox()
        self.channels_label = QLabel('Channels:')
        self.channels_input = QComboBox()
        self.samplerate_label = QLabel('Sample rate:')
        self.samplerate_input = QComboBox()
        self.volume_label = QLabel('Volume:')
        self.volume_input = QComboBox()
        self.languagechannel_label = QLabel('Language Channel:')
        self.languagechannel_input = QLineEdit()
        self.speed_label = QLabel('Speed:')
        self.speed_input = QLineEdit()

        self.search_button = SearchButton('Convert')
        self.play_button = SearchButton('Play converted audio')
        self.download_button = SearchButton('Download converted audio')

        # Add to the upper left layout
        upper_left_layout.addWidget(audio_path_label)
        upper_left_layout.addWidget(self.audio_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(self.outputformat_label)
        upper_left_layout.addWidget(self.outputformat_input)
        upper_left_layout.addWidget(self.bitrate_label)
        upper_left_layout.addWidget(self.bitrate_input)
        upper_left_layout.addWidget(self.channels_label)
        upper_left_layout.addWidget(self.channels_input)
        upper_left_layout.addWidget(self.samplerate_label)
        upper_left_layout.addWidget(self.samplerate_input)
        upper_left_layout.addWidget(self.volume_label)
        upper_left_layout.addWidget(self.volume_input)
        upper_left_layout.addWidget(self.languagechannel_label)
        upper_left_layout.addWidget(self.languagechannel_input)
        upper_left_layout.addWidget(self.speed_label)
        upper_left_layout.addWidget(self.speed_input)

        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addWidget(self.play_button)
        upper_left_layout.addWidget(self.download_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

        self.update_comboBoxes()
    
    def update_comboBoxes(self):
        self.outputformat_input.clear()
        self.bitrate_input.clear()
        self.channels_input.clear()
        self.samplerate_input.clear()
        self.volume_input.clear()
        self.languagechannel_input.clear()
        self.volume_input.clear()
        with open('data/audio_options/format.txt', 'r') as file:
            words = file.read().splitlines()
        self.outputformat_input.addItems(words)
        with open('data/audio_options/bit_rate.txt', 'r') as file:
            words = file.read().splitlines()
        self.bitrate_input.addItems(words)
        with open('data/audio_options/audio_channels.txt', 'r') as file:
            words = file.read().splitlines()
        self.channels_input.addItems(words)
        with open('data/audio_options/sample_rate.txt', 'r') as file:
            words = file.read().splitlines()
        self.samplerate_input.addItems(words)
        with open('data/audio_options/volume.txt', 'r') as file:
            words = file.read().splitlines()
        self.volume_input.addItems(words)

    # Getters
    def get_video_path(self):
        return self.video_path_input.text()
    
    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
