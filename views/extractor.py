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

        # Conectar la señal del right_arrow_clicked con el método de apertura de una nueva ventana
        self.nav_widget.left_arrow_clicked.connect(self.open_right_window)
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

        # Crear una instancia de CenterLayout
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your file and let the system handle the rest. Using advanced algorithms, the extractor analyzes the file and retrieves all available metadata, including file type, size, creation and modification dates, author information, and more. This tool provides a clear and organized summary of the data embedded in your file, giving you quick insights without any additional effort."
        )

        # Initially hide right_layout and show center_widget
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)  # Asignar el layout a un widget contenedor
        self.right_widget.hide()  # Inicialmente ocultamos el RightLayout

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
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_images import VideoToImagesView

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = VideoToImagesView()
        self.new_window.show()

    def open_left_window(self):
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.audio_to_audio import AudioToAudioView

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = AudioToAudioView()
        self.new_window.show()

    def update_function_name(self, new_name):
        # Llamar al método del NavWidget para actualizar el nombre
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save(self):
        # muestra para seleccionar archivo, tambien lo guarda en carpeta input_files
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                "Todos los archivos (*.*)")

        # Si se selecciona un archivo, se muestra su ruta en el input
        if self.file_path:
            # Call the function to send the file to the API
            self.file_path = self.file_path
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.file_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")


    def searchResults(self):

        # Verifica que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún archivo.")
            return

        # Clear the rows before processing
        self.right_layout.clear_rows()

        self.center_widget.show()
        self.right_widget.hide()

        # Process initialized
        self.center_widget.change_label_text("Processing file... Please wait")
        QApplication.processEvents()

        endpoint = '/api/get-metadata'
        # Envía el video a la API y obtiene la respuesta
        response = send_to_ConvertService_GetMetadata(self.file_path, endpoint)
        print (response)
        if response:

            for key, value in response.items():
                # Añadir valores exttraidos a la tabla
                self.result_matrix = [key, value]
                self.showNewRow()

            self.center_widget.hide()
            self.right_widget.show()

            self.process_complete()
                
        else:
            QMessageBox.critical(self, "Error", "Error al procesar el archivo.")
            self.center_widget.change_label_text("Upload your file and let the system handle the rest. Using advanced algorithms, the extractor analyzes the file and retrieves all available metadata, including file type, size, creation and modification dates, author information, and more. This tool provides a clear and organized summary of the data embedded in your file, giving you quick insights without any additional effort.")
            QApplication.processEvents()

    def showNewRow(self):
        self.right_layout.add_new_row(self.result_matrix)
        #implementar para que pasen las filas que devuelvan
        


    def start_process(self):
        # Crear un cuadro de diálogo sin botones
        self.progress_dialog = QDialog(self)
        self.progress_dialog.setWindowTitle("Processing")
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setFixedSize(300, 100)

        # Agregar un texto informativo
        layout = QVBoxLayout()
        label = QLabel("Your video is being processed, please wait...")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.progress_dialog.setLayout(layout)

        # Mostrar el cuadro de diálogo
        self.progress_dialog.show()
        
    def process_interrupted(self):
        # Interrumpe proceso y cierra cuadro de diálogo
        self.progress_dialog.close()

    def process_complete(self):
        # Cierra el cuadro de diálogo
        self.progress_dialog.close()
        QMessageBox.information(self, "Completed", "The process has completed successfully.")