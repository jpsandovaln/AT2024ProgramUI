import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressDialog
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

        # Layout general (usamos un nuevo layout para esta vista)
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
        self.upper_left_area.browse_button.clicked.connect(self.show_path_and_save_audio)
        self.upper_left_area.search_button.clicked.connect(self.searchResults)
        self.upper_left_area.play_button.clicked.connect(self.playVideo)
        self.upper_left_area.download_button.clicked.connect(self.downloadVideo)

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

    def show_path_and_save_audio(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos (*.mp3 *.mov *.avi *.mkv *.flv *.webm *.ogg *.wmv)")
        if self.file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.audio_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")

    def searchResults(self):
        # Verifica que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún archivo.")
            return
        
        self.format = self.upper_left_area.outputformat_input.currentText()
        if not self.format:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún formato de salida.")
            return

        bitrate = self.upper_left_area.bitrate_input.currentText()
        channels = self.upper_left_area.channels_input.currentText()
        samplerate = self.upper_left_area.samplerate_input.currentText()
        volume = self.upper_left_area.volume_input.currentText()
        languagechannel = self.upper_left_area.languagechannel_input.text()
        speed = self.upper_left_area.speed_input.text()

        # Process Window initialized
        self.start_process()

        endpoint = '/api/convert-audio'
        # Envía el video a la API y obtiene la respuesta
        response = send_to_ConvertService_AudioToAudio(self.file_path,  endpoint, self.format, bitrate, channels, samplerate, volume, languagechannel, speed)
        print (response)

        if response and response.get("download_URL"):
            # Extrae la URL de descarga de la respuesta
            video_url = response["download_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta, el folder extraido y el nombre del zip file
            self.file_info = download_media(video_url)

            # Watch video
            self.upper_left_area.play_button.show()
            self.upper_left_area.download_button.show()
            
            self.process_complete()
    
    def playVideo(self):
        # Crear y mostrar la ventana del reproductor de video
        self.video_player_window = VideoPlayer(self.file_info)

        # Mostrar la ventana del reproductor
        self.video_player_window.show()
        self.video_player_window.play_video()

    def downloadVideo(self):
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(self.format)  # Puedes cambiar la extensión por la que corresponda a tu archivo
        file_info, _ = file_dialog.getSaveFileName(self, "Guardar video", "", f"Archivos de video (*.{self.format});;Todos los archivos (*)")
        
        if file_info:  # Verifica si el usuario seleccionó un archivo
            try:
                # Copia el archivo desde la ubicación original a la nueva ubicación seleccionada por el usuario
                shutil.copy(self.file_info, file_info)
                print(f"El archivo se ha guardado en: {file_info}")
                QMessageBox.accepted(self, "Saved", "File saved")
            except Exception as e: # REVISAR
                print(f"Error al guardar el archivo: {e}")

    def start_process(self):
        # Crea el cuadro de diálogo "Procesando"
        self.progress_dialog = QProgressDialog("Procesando, por favor espere...", None, 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButtonText(None)
        self.progress_dialog.setWindowTitle("Procesando")
        self.progress_dialog.setRange(0, 0)  # Indeterminado
        self.progress_dialog.show()
        
    def process_interrupted(self):
        # Interrumpe proceso y cierra cuadro de diálogo
        self.progress_dialog.close()

    def process_complete(self):
        # Cierra el cuadro de diálogo
        self.progress_dialog.close()
        QMessageBox.information(self, "Completado", "El proceso ha finalizado con éxito.")