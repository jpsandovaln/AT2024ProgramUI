from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox
from BlueButton import BlueButton


class UpperLeftArea(QWidget):
    def __init__(self):
        # Constructor inherits and creates upper left area
        super().__init__()
        self.create_upper_left_area()

    def create_upper_left_area(self):
        upper_left_layout = QVBoxLayout()

        # Creating labels , inputs and buttons
        video_path_label = QLabel('Video Path:')
        word_label = QLabel('Word:')
        neural_network_model_label = QLabel('Type of Recognizer:')
        percentage_label = QLabel('Percentage')
        self.video_path_input = QLineEdit()
        self.video_path_input.setReadOnly(True)  # It  doesn't allow to edit
        self.word_input = QComboBox()
        
        self.neural_network_model_combobox = QComboBox()
        self.neural_network_model_combobox.addItems(['Object Recognizer', 'Gender Recognizer', 'Face Recognizer'])
        self.neural_network_model_combobox.currentIndexChanged.connect(self.update_word_input)
        self.percentage_combobox = QComboBox()
        self.percentage_combobox.addItems(['10', '20', '50', '70', '80'])
        self.browse_button = BlueButton('Browse')
        self.search_button = BlueButton('Search')

        # Add to the upper left layout
        upper_left_layout.addWidget(video_path_label)
        upper_left_layout.addWidget(self.video_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(neural_network_model_label)
        upper_left_layout.addWidget(self.neural_network_model_combobox)
        upper_left_layout.addWidget(word_label)
        upper_left_layout.addWidget(self.word_input)
        upper_left_layout.addWidget(percentage_label)
        upper_left_layout.addWidget(self.percentage_combobox)
        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

        self.update_word_input()

    # Updates the word_input options based on the selected option from neural_network_model
    def update_word_input(self):
        selected_model = self.get_neural_network_model()
        self.word_input.clear()

        if selected_model == 'Object Recognizer':
            self.word_input.addItems([
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow",
            "diningtable", "dog", "horse", "motorbike", "person",
            "pottedplant", "sheep", "sofa", "train", "tvmonitor"
            ])
        elif selected_model == 'Gender Recognizer':
            self.word_input.addItems(['Male', 'Female'])
        elif selected_model == 'Face Recognizer':
            self.word_input.clear()

    # Getters
    def get_video_path(self):
        return self.video_path_input.text()

    def get_word(self):
        return self.word_input.currentText()

    def get_neural_network_model(self):
        return self.neural_network_model_combobox.currentText()

    def get_percentage_label(self):
        return self.percentage_combobox.currentText()
