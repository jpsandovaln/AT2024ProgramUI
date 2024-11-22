from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea4 import UpperLeftArea4
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from components.VideoPlayer import VideoPlayer
from api.api_requests import send_to_ConvertService_AudioToAudio
from utils.file_utils import download_media
from utils.SaveFile import SaveFile
from utils.ImageDialog import ImageDialog
import shutil


class AudioToAudioView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        
        # Configure the specific title for this view
        self.setWindowTitle('Audio To Audio Converter')
        self.setGeometry(100, 100, 1000, 700)

        # General layout (we used a new layout for this view)
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

        self.update_function_name('Audio to Audio Converter')

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)

        # Left area with labels and buttons
        self.upper_left_area = UpperLeftArea4()
        self.upper_left_area.play_button.hide()
        self.upper_left_area.download_button.hide()

        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Center widget (displays an icon and message)
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your audio file and specify the desired output parameters, including format, bit rate, number of channels, sample rate, volume adjustment, language channel, and playback speed. The system will process your input audio and convert it into the specified format, ensuring compatibility with your preferences while maintaining optimal sound quality."
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
        self.upper_left_area.play_button.clicked.connect(self.play)
        self.upper_left_area.download_button.clicked.connect(self.download)

    def open_right_window(self):
        from views.video_to_images import VideoToImagesView
        self.close()
        self.new_window = VideoToImagesView()
        self.new_window.show()
    
    def open_left_window(self):
        from views.image_to_image import ImageToImageView
        self.close()
        self.new_window = ImageToImageView()
        self.new_window.show()

    def update_function_name(self, new_name):
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Archivos (*.mp3 *.mov *.avi *.mkv *.flv *.webm *.ogg *.wmv)")
        if self.file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.audio_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")

    def searchResults(self):
        # Verificar que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No file selected.")
            return
        
        # Verificar que se haya seleccionado un formato de salida
        self.format = self.upper_left_area.outputformat_input.currentText()
        if not self.format:
            QMessageBox.critical(self, "Error", "No output format has been selected.")
            return

        bitrate = self.upper_left_area.bitrate_input.currentText()
        channels = self.upper_left_area.channels_input.currentText()
        samplerate = self.upper_left_area.samplerate_input.currentText()
        volume = self.upper_left_area.volume_input.currentText()
        languagechannel = self.upper_left_area.languagechannel_input.text()
        speed = self.upper_left_area.speed_input.text()

        # Validar que speed no exceda el límite (2.0)
        try:
            speed = float(speed)  # Convertir a número flotante
            if speed > 2.0 or speed <= 0:
                QMessageBox.critical(self, "Error", "Playback speed must be between 0.1 and 2.0.")
                return
        except ValueError:
            QMessageBox.critical(self, "Error", "Playback speed must be a valid number.")
            return

        # Validar que languagechannel sea un valor numérico
        if not languagechannel.isdigit():
            QMessageBox.critical(self, "Error", "The language channel must be a numeric value.")
            return


        # Mostrar mensaje de "procesando"
        self.center_widget.change_label_text("Processing audio... Please wait")
        QApplication.processEvents()

        endpoint = '/api/convert-audio'
        # Llamar a la API
        response = send_to_ConvertService_AudioToAudio(
            self.file_path, endpoint, self.format, bitrate, channels, samplerate, volume, languagechannel, speed
        )

        # Manejo de la respuesta
        if response and response.get("download_URL"):
            video_url = response["download_URL"]
            self.file_info = download_media(video_url)
            self.upper_left_area.play_button.show()
            self.upper_left_area.download_button.show()
            QMessageBox.information(self, "Completed", "The process has completed successfully.")
            self.center_widget.change_label_text("Upload your audio file and specify the desired output parameters, including format, bit rate, number of channels, sample rate, volume adjustment, language channel, and playback speed. The system will process your input audio and convert it into the specified format, ensuring compatibility with your preferences while maintaining optimal sound quality.")
        else:
            QMessageBox.critical(self, "Error", "Error processing audio.")
            self.center_widget.change_label_text("Upload your audio file and specify the desired output parameters, including format, bit rate, number of channels, sample rate, volume adjustment, language channel, and playback speed.")
        QApplication.processEvents()
        
    
    def play(self):
        # Create and display the audio player window
        self.player_window = VideoPlayer(self.file_info)

        # Show the player window
        self.player_window.show()
        self.player_window.play_video()

    def download(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(self.format)
        file_info, _ = file_dialog.getSaveFileName(self, "Save file", "", f"Archivos de video (*.{self.format});;Todos los archivos (*)")
        
        if file_info:  # Check if the user selected a file
            try:
                # Copy the file from the original location to the new location selected by the user
                shutil.copy(self.file_info, file_info)
                print(f"The file has been saved in: {file_info}")
                QMessageBox.accepted(self, "Saved", "File saved")
            except Exception as e:
                print(f"Error saving file: {e}")