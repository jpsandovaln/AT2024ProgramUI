from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea2 import UpperLeftArea2
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from components.VideoPlayer import VideoPlayer
from api.api_requests import send_to_ConvertService_VideoToVideo
from utils.file_utils import download_media
from utils.SaveFile import SaveFile
from utils.ImageDialog import ImageDialog
import shutil


class VideoToVideoView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        
        # Configure the specific title for this view
        self.setWindowTitle('Video to Video Converter')
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

        self.update_function_name('Video to Video Converter')

        # Main Horizontal Layout
        main_layout = QHBoxLayout()

        # Left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)

        # Left area with labels and buttons
        self.upper_left_area = UpperLeftArea2()
        self.upper_left_area.play_button.hide()
        self.upper_left_area.download_button.hide()

        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Center widget (displays an icon and message)
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your video and specify the desired output parameters, including format, FPS (frames per second), video codec, audio codec, and audio channels. The system will process the input video and convert it into the specified format, ensuring compatibility with your requirements and maintaining high-quality output."
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
        from views.image_to_image import ImageToImageView
        self.close()
        self.new_window = ImageToImageView()
        self.new_window.show()
    
    def open_left_window(self):
        from views.video_to_images import VideoToImagesView
        self.close()
        self.new_window = VideoToImagesView()
        self.new_window.show()

    def update_function_name(self, new_name):
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save(self):
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Seleccionar archivo", 
            "", 
            "Archivos de video (*.avi *.flv *.mkv *.mov *.mp4 *.ogg *.webm *.wmv)"
        )
        if self.file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.video_path_input.setText(self.file_path)
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

        fps = self.upper_left_area.fps_input.text()
        vcodec = self.upper_left_area.vcodec_input.currentText()
        acodec = self.upper_left_area.acodec_input.currentText()
        achannel = self.upper_left_area.achannel_input.currentText()

        # Clear the rows before processing
        self.right_layout.clear_rows()

        # Process initialized
        self.center_widget.change_label_text("Processing video... Please wait")
        QApplication.processEvents()

        endpoint = '/api/video-to-video'
        # Envía el video a la API y obtiene la respuesta
        response = send_to_ConvertService_VideoToVideo(self.file_path, endpoint, self.format, fps, vcodec, acodec, achannel)
        print (response)

        if response and response.get("download_URL"):
            # Extrae la URL de descarga de la respuesta
            video_url = response["download_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta, el folder extraido y el nombre del zip file
            self.file_info = download_media(video_url)

            # Watch video
            self.upper_left_area.play_button.show()
            self.upper_left_area.download_button.show()
            
            QMessageBox.information(self, "Completed", "The process has completed successfully.")
            self.center_widget.change_label_text("Upload your video and specify the desired output parameters, including format, FPS (frames per second), video codec, audio codec, and audio channels. The system will process the input video and convert it into the specified format, ensuring compatibility with your requirements and maintaining high-quality output.")
            QApplication.processEvents()
        else:
            QMessageBox.critical(self, "Error", "Error al procesar el video.")
            self.center_widget.change_label_text("Upload your video and specify the desired output parameters, including format, FPS (frames per second), video codec, audio codec, and audio channels. The system will process the input video and convert it into the specified format, ensuring compatibility with your requirements and maintaining high-quality output.")
            QApplication.processEvents()
    
    def play(self):
        # Crear y mostrar la ventana del reproductor de video
        self.player_window = VideoPlayer(self.file_info)

        # Mostrar la ventana del reproductor
        self.player_window.show()
        self.player_window.play_video()

    def download(self):
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