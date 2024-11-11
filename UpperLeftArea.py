from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox
from BlueButton import BlueButton


class UpperLeftArea(QWidget):
    def __init__(self):
        # constructor hereda y llama a crear un area superior izquierda
        super().__init__()
        self.create_upper_left_area()

    def create_upper_left_area(self):
        upper_left_layout = QVBoxLayout()

        # Creating labels , inputs and buttons
        video_path_label = QLabel('Video Path:')
        word_label = QLabel('Word:')
        neural_network_model_label = QLabel('Neural network Model')
        percentage_label = QLabel('Percentage')
        self.video_path_input = QLineEdit()
        self.video_path_input.setReadOnly(True)  # para que no se pueda editar
        self.word_input = QLineEdit()
        self.word_input.setClearButtonEnabled(True)
        self.word_input.setMaxLength(300)
        self.neural_network_model_combobox = QComboBox()
        self.neural_network_model_combobox.addItem('Deepface')
        self.neural_network_model_combobox.addItem('Yolo')
        self.percentage_combobox = QComboBox()
        self.percentage_combobox.addItem('10')
        self.percentage_combobox.addItem('20')
        self.percentage_combobox.addItem('50')
        self.percentage_combobox.addItem('70')
        self.percentage_combobox.addItem('80')
        self.browse_button = BlueButton('Browse')
        self.search_button = BlueButton('Search')

        # Add to the upper left layout
        upper_left_layout.addWidget(video_path_label)
        upper_left_layout.addWidget(self.video_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(word_label)
        upper_left_layout.addWidget(self.word_input)
        upper_left_layout.addWidget(neural_network_model_label)
        upper_left_layout.addWidget(self.neural_network_model_combobox)
        upper_left_layout.addWidget(percentage_label)
        upper_left_layout.addWidget(self.percentage_combobox)
        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

    # Getters
    def get_video_path(self):
        return self.video_path_input.text()

    def get_word(self):
        return self.word_input.text()

    def get_neural_network_model(self):
        return self.neural_network_model_combobox.currentText()

    def get_percentage_label(self):
        return self.percentage_combobox.currentText()
