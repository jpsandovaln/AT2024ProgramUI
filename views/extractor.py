from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea5 import UpperLeftArea5
from components.RigthLayout2 import Rigthlayout2
from components.CenterLayout import CenterLayout
from api.api_requests import send_to_ConvertService_GetMetadata
from utils.SaveFile import SaveFile


class ExtractorView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        # Window configurations
        self.setWindowTitle('Metadata Extractor')
        self.setGeometry(100, 100, 1000, 700)

        # General Layout
        overall_layout = QVBoxLayout()
        overall_layout.setContentsMargins(0, 0, 0, 10)
        overall_layout.setSpacing(0)

        # Header widget in the top side
        header_widget = HeaderWidget("./assets/img/logo.png")
        overall_layout.addWidget(header_widget)

        # Nav layout under Header
        self.nav_widget = NavWidget()
        overall_layout.addWidget(self.nav_widget)

        # Connect the right_arrow_clicked signal to the opening method of a new window
        self.nav_widget.left_arrow_clicked.connect(self.open_left_window)
        self.nav_widget.right_arrow_clicked.connect(self.open_right_window)

        self.update_function_name('Metadata Extractor')

        # Main Horizontal Layout 
        main_layout = QHBoxLayout()

        # Main left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)
        
        # Left area of labels and buttons
        self.upper_left_area = UpperLeftArea5()
        
        # Add areas into left layout
        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout2()

        # Create an instance of CenterLayout
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your file and let the system handle the rest. Using advanced algorithms, the extractor analyzes the file and retrieves all available metadata, including file type, size, creation and modification dates, author information, and more. This tool provides a clear and organized summary of the data embedded in your file, giving you quick insights without any additional effort."
        )

        # Initially hide right_layout and show center_widget
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)  # Assign the layout to a container widget
        self.right_widget.hide()  # Initially we hide the RightLayout

        # Add the layouts into the main layout
        main_layout.addLayout(left_layout, 1)  #  1 is the expansion factor 
        main_layout.addWidget(self.center_widget, 3, alignment=Qt.AlignCenter)  # 3 is the expansion factor for the center_widget
        main_layout.addWidget(self.right_widget, 3) 
        # Add main_layout into overall_layout
        overall_layout.addLayout(main_layout)

        # Add overall layout into window
        self.setLayout(overall_layout)

        # Triggers
        self.upper_left_area.browse_button.clicked.connect(self.show_path_and_save)
        self.upper_left_area.search_button.clicked.connect(self.searchResults)
        

    def open_right_window(self):
        # Import only when necessary
        from views.video_to_images import VideoToImagesView

        # Close the main window
        self.close()

        # Create and display the new window
        self.new_window = VideoToImagesView()
        self.new_window.show()

    def open_left_window(self):
        # Import only when necessary
        from views.audio_to_audio import AudioToAudioView

        # Close the main window
        self.close()

        # Create and display the new window
        self.new_window = AudioToAudioView()
        self.new_window.show()

    def update_function_name(self, new_name):
        # Call the NavWidget method to update the name
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save(self):
        # shows to select file, also saves it in input_files folder
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "",
                                                "Todos los archivos (*.*)")

        # If a file is selected, its path is shown in the input
        if self.file_path:
            # Call the function to send the file to the API
            self.file_path = self.file_path
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.file_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Something went wrong while opening the file, most likely 'Cancel' was pressed")


    def searchResults(self):

        # Verify that a file has been selected
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No file selected.")
            return

        # Clear the rows before processing
        self.right_layout.clear_rows()

        self.center_widget.show()
        self.right_widget.hide()

        # Process initialized
        self.center_widget.change_label_text("Processing file... Please wait")
        QApplication.processEvents()

        endpoint = '/api/get-metadata'
        # Send the video to the API and get the response
        response = send_to_ConvertService_GetMetadata(self.file_path, endpoint)
        print (response)
        if response:

            for key, value in response.items():
                # Add extracted values ​​to the table
                self.result_matrix = [key, value]
                self.showNewRow()

            self.center_widget.hide()
            self.right_widget.show()

            QMessageBox.information(self, "Completed", "The process has completed successfully.")
            self.center_widget.change_label_text("Upload your file and let the system handle the rest. Using advanced algorithms, the extractor analyzes the file and retrieves all available metadata, including file type, size, creation and modification dates, author information, and more. This tool provides a clear and organized summary of the data embedded in your file, giving you quick insights without any additional effort.")
            QApplication.processEvents()

        else:
            QMessageBox.critical(self, "Error", "Error processing file.")
            self.center_widget.change_label_text("Upload your file and let the system handle the rest. Using advanced algorithms, the extractor analyzes the file and retrieves all available metadata, including file type, size, creation and modification dates, author information, and more. This tool provides a clear and organized summary of the data embedded in your file, giving you quick insights without any additional effort.")
            QApplication.processEvents()

    def showNewRow(self):
        self.right_layout.add_new_row(self.result_matrix)
        