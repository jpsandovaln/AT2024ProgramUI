from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QLabel, \
    QLineEdit, QComboBox, QCheckBox
from .Button import Button, SearchButton


class UpperLeftArea3(QWidget):
    def __init__(self):
        # Constructor inherits and creates upper left area
        super().__init__()
        self.create_upper_left_area()

    def create_upper_left_area(self):
        upper_left_layout = QVBoxLayout()

        # Creating labels , inputs and buttons
        image_path_label = QLabel('Image Path:')
        self.image_path_input = QLineEdit()
        self.image_path_input.setReadOnly(True)
        self.browse_button = Button('Browse')
        self.outputformat_label = QLabel('Format to convert:')
        self.outputformat_input = QComboBox()
        self.resizew_label = QLabel('Resize width:')
        self.resizew_input = QLineEdit()
        self.resizeh_label = QLabel('Resize height:')
        self.resizeh_input = QLineEdit()
        self.resizetype_label = QLabel('Resize type:')
        self.resizetype_input = QComboBox()
        self.rotate_label = QLabel('Rotate (deg):')
        self.rotate_input = QLineEdit()
        filters_label = QLabel('FILTERS:')
        self.grayscale_checkbox = QCheckBox("Grayscale", self)
        self.blur_checkbox = QCheckBox("Blur", self)
        self.contour_checkbox = QCheckBox("Contour", self)
        self.detail_checkbox = QCheckBox("Detail", self)
        self.edge_enhance_checkbox = QCheckBox("Edge enhance", self)
        self.edge_enhance_more_checkbox = QCheckBox("Edge enhance more", self)
        self.emboss_checkbox = QCheckBox("Emboss", self)
        self.find_edges_checkbox = QCheckBox("Find edges", self)
        self.sharpen_checkbox = QCheckBox("Sharpen", self)
        self.smooth_checkbox = QCheckBox("Smooth", self)
        self.smooth_more_checkbox = QCheckBox("Smooth more", self)

        self.search_button = SearchButton('Convert')
        self.download_button = SearchButton('Download converted image')

        # Add to the upper left layout
        upper_left_layout.addWidget(image_path_label)
        upper_left_layout.addWidget(self.image_path_input)
        upper_left_layout.addWidget(self.browse_button)
        upper_left_layout.addWidget(self.outputformat_label)
        upper_left_layout.addWidget(self.outputformat_input)
        upper_left_layout.addWidget(self.resizew_label)
        upper_left_layout.addWidget(self.resizew_input)
        upper_left_layout.addWidget(self.resizeh_label)
        upper_left_layout.addWidget(self.resizeh_input)
        upper_left_layout.addWidget(self.resizetype_label)
        upper_left_layout.addWidget(self.resizetype_input)
        upper_left_layout.addWidget(self.rotate_label)
        upper_left_layout.addWidget(self.rotate_input)
        upper_left_layout.addWidget(filters_label)
        upper_left_layout.addWidget(self.grayscale_checkbox)
        upper_left_layout.addWidget(self.blur_checkbox)
        upper_left_layout.addWidget(self.contour_checkbox)
        upper_left_layout.addWidget(self.detail_checkbox)
        upper_left_layout.addWidget(self.edge_enhance_checkbox)
        upper_left_layout.addWidget(self.edge_enhance_more_checkbox)
        upper_left_layout.addWidget(self.emboss_checkbox)
        upper_left_layout.addWidget(self.find_edges_checkbox)
        upper_left_layout.addWidget(self.sharpen_checkbox)
        upper_left_layout.addWidget(self.smooth_checkbox)
        upper_left_layout.addWidget(self.smooth_more_checkbox)

        upper_left_layout.addWidget(self.search_button)
        upper_left_layout.addWidget(self.download_button)
        upper_left_layout.addStretch()

        # Adding layout to widget
        self.setLayout(upper_left_layout)

        self.update_comboBoxes()
    
    def update_comboBoxes(self):
        self.outputformat_input.clear()
        with open('data/imageFormatOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.outputformat_input.addItems(words)
        self.resizetype_input.clear()
        with open('data/resizeTypeOptions.txt', 'r') as file:
            words = file.read().splitlines()
        self.resizetype_input.addItems(words)

    # Getters
    def get_video_path(self):
        return self.image_path_input.text()

    def get_word(self):
        return self.word_input.currentText()

    def get_percentage_label(self):
        return self.percentage_combobox.currentText()
    
    # Getter
    def get_image_path(self):
        return self.image_path_input.text()
