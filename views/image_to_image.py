import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea3 import UpperLeftArea3
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from api.api_requests import send_to_ConvertService_ImageToImage
from utils.file_utils import download_media
from utils.SaveFile import SaveFile
import shutil


class ImageToImageView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        
        # Configure the specific title for this view
        self.setWindowTitle('Image to Image Converter')
        self.setGeometry(100, 100, 1000, 700)

        # Layout general
        overall_layout = QVBoxLayout()
        overall_layout.setContentsMargins(0, 0, 0, 10)
        overall_layout.setSpacing(0)

        # Header widget
        header_widget = HeaderWidget("./assets/img/logo.png")
        overall_layout.addWidget(header_widget)

        # Nav widget (below the header)
        self.nav_widget = NavWidget()
        overall_layout.addWidget(self.nav_widget)

        # Connect navigation signals to handle window switching
        self.nav_widget.left_arrow_clicked.connect(self.open_left_window)
        self.nav_widget.right_arrow_clicked.connect(self.open_right_window)

        self.update_function_name('Image to Image Converter')

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)

        # Left area with labels and buttons
        self.upper_left_area = UpperLeftArea3()
        self.upper_left_area.download_button.hide()

        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Center widget (displays an icon and message)
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your image and specify the desired output parameters, including resize width, resize height, resize type, rotation, format, rotation angle, grayscale conversion, and filters. The system will process the input image according to the specified settings, adjusting its dimensions, format, and visual properties to meet your needs while preserving image quality and ensuring the desired effect."
        )

        # Initially hide right_layout and show center_widget
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.hide()

        # Add all layouts to the main layout
        main_layout.addLayout(left_layout, 1)  # 1 is the expansion factor
        main_layout.addWidget(self.center_widget, 3, alignment=Qt.AlignCenter)  # Center widget
        main_layout.addWidget(self.right_widget, 3)  # Right layout

        # Add the main layout into the overall layout
        overall_layout.addLayout(main_layout)

        # Set the overall layout to the window (cleaner handling of layout)
        self.setLayout(overall_layout)

        # Connect triggers to handle actions
        self.upper_left_area.browse_button.clicked.connect(self.show_path_and_save)
        self.upper_left_area.search_button.clicked.connect(self.searchResults)
        self.upper_left_area.download_button.clicked.connect(self.downloadImage)

    def open_right_window(self):
        # Import only when necessary
        from views.audio_to_audio import AudioToAudioView

        # Close the main window
        self.close()

        # Create and display the new window
        self.new_window = AudioToAudioView()
        self.new_window.show()
    
    def open_left_window(self):
        from views.video_to_video import VideoToVideoView
        self.close()
        self.new_window = VideoToVideoView()
        self.new_window.show()

    def update_function_name(self, new_name):
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select file", 
            "", 
            "Archivos de imagen (*.jpg *.jpeg *.png *.gif)"
        )
        if self.file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.image_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")

    def searchResults(self):

        # Verify that a file has been selected
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No file selected.")
            return
        
        self.format = self.upper_left_area.outputformat_input.currentText()
        resizetype = self.upper_left_area.resizetype_input.currentText()
        resizew = self.upper_left_area.resizew_input.text()
        resizeh = self.upper_left_area.resizeh_input.text()
        rotate = self.upper_left_area.rotate_input.text()
        grayscale = self.upper_left_area.grayscale_checkbox.isChecked()
        blur = self.upper_left_area.blur_checkbox.isChecked()
        contour = self.upper_left_area.contour_checkbox.isChecked()
        detail = self.upper_left_area.detail_checkbox.isChecked()
        edge_enhance = self.upper_left_area.edge_enhance_checkbox.isChecked()
        edge_enhance_more = self.upper_left_area.edge_enhance_more_checkbox.isChecked()
        emboss = self.upper_left_area.emboss_checkbox.isChecked()
        find_edges = self.upper_left_area.find_edges_checkbox.isChecked()
        sharpen = self.upper_left_area.sharpen_checkbox.isChecked()
        smooth = self.upper_left_area.smooth_checkbox.isChecked()
        smooth_more = self.upper_left_area.smooth_more_checkbox.isChecked()

        # Process Window initialized
        self.center_widget.change_label_text("Processing image... Please wait")
        QApplication.processEvents()

        endpoint = '/api/image-configuration'
        # Send the video to the API and get the response
        response = send_to_ConvertService_ImageToImage(
            self.file_path,             # Original image path
            endpoint,                   # Endpoint to conversion service
            self.format,                # Output format
            resize_type = resizetype,   # Optional: Resize type
            resize_width=resizew,       # Optional: Image width
            resize_height=resizeh,      # Optional: Image height
            rotate_angle=rotate,        # Optional: Rotation angle
            grayscale=grayscale,        # Optional: Convert to grayscale
            blur=blur,                  # Optional: blur filter
            contour=contour,            # Optional: contour filter
            detail=detail,              # Optional: Details filter
            edge_enhance=edge_enhance,  # Optional: Edge Enhancement Filter
            edge_enhance_more=edge_enhance_more, # Optional: More edge enhancement filter
            emboss=emboss,              # Optional: emboss filter
            find_edges=find_edges,      # Optional: Find edges filter
            sharpen=sharpen,            # Optional: Sharpening Enhancement Filter
            smooth=smooth,              # Optional: smoothing filter
            smooth_more=smooth_more     # Optional: more smoothing filter
        )

        print (response)

        if response and response.get("download_URL"):
            # Extract the download URL from the response
            image_url = response["download_URL"]

            # Download the ZIP file and save its absolute path, the extracted folder and the name of the zip file
            self.file_info = download_media(image_url)

            self.upper_left_area.download_button.show()
            
            QMessageBox.information(self, "Completed", "The process has completed successfully.")
            self.center_widget.change_label_text("Upload your image and specify the desired output parameters, including resize width, resize height, resize type, rotation, format, rotation angle, grayscale conversion, and filters. The system will process the input image according to the specified settings, adjusting its dimensions, format, and visual properties to meet your needs while preserving image quality and ensuring the desired effect.")
            QApplication.processEvents()
        else:
            QMessageBox.critical(self, "Error", "Error processing image.")
            self.center_widget.change_label_text("Upload your image and specify the desired output parameters, including resize width, resize height, resize type, rotation, format, rotation angle, grayscale conversion, and filters. The system will process the input image according to the specified settings, adjusting its dimensions, format, and visual properties to meet your needs while preserving image quality and ensuring the desired effect.")
            QApplication.processEvents()

    def downloadImage(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(self.format if self.format.startswith('.') else f'.{self.format}')
        
        # File filter
        file_info, _ = file_dialog.getSaveFileName(self, "Save file", "", 
                                                f"Archivos de imágenes (*.{self.format});;Todos los archivos (*)")
        
        if file_info:  # Check if the user selected a file
            try:
                # Verify that the source path is valid
                if not os.path.exists(self.file_info):
                    raise Exception(f"The file does not exist in the path: {self.file_info}")
                
                # If the format is not present in the file name, add the extension
                if not file_info.endswith(self.format):
                    file_info = f"{file_info}.{self.format}"
                
                # Copy the file from the original location to the new location selected by the user
                shutil.copy(self.file_info, file_info)
                print(f"The file has been saved in: {file_info}")

                # Display a success message using QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("File saved")
                msg.setWindowTitle("Saved")
                msg.exec_()

            except Exception as e: 
                
                # Display a success message using QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText(f"Error saving file: {e}")
                msg.setWindowTitle("Error")
                msg.exec_()