import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QDialog, QLabel, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea import UpperLeftArea
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from components.VideoPlayer import VideoPlayer
from api.api_requests import send_to_ConvertService, send_to_MLservice, send_file_to_MLservice
from utils.file_utils import download_file
from utils.SaveFile import SaveFile
from utils.ImageDialog import ImageDialog
from logic.time import seconds_to_hms


class VideoToImagesView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        # Window configurations
        self.setWindowTitle('Video Frames Analyzer')
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

        self.update_function_name('Video Frame Analyzer')

        # Main Horizontal Layout 
        main_layout = QHBoxLayout()

        # Main left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)
        
        # Left area of labels and buttons
        self.upper_left_area = UpperLeftArea()
        
        # Add areas into left layout
        left_layout.addWidget(self.upper_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Crear una instancia de CenterLayout
        self.center_widget = CenterLayout(
            image_path="./assets/icons/cloud-download.png",
            label_text="Upload your video and select the object, face, or person (male or female) you want to search for. Using Machine Learning, the system analyzes each frame of the video and provides a list of results where the selected object, face, or person is detected, helping you find exactly what you're looking for in the video."
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
        self.upper_left_area.browse_button.clicked.connect(self.show_path_and_save_image)
        self.upper_left_area.search_button.clicked.connect(self.searchResults)
        self.right_layout.show_image_button.clicked.connect(self.showImage)
        self.right_layout.show_video_point_button.clicked.connect(self.showInVideo)
        self.upper_left_area.browse_image_button.clicked.connect(self.upload_image_path_and_save)


    def open_right_window(self):
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_video import VideoToVideoView

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = VideoToVideoView()
        self.new_window.show()

    def open_left_window(self):
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_video import VideoToVideoView

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = VideoToVideoView()
        self.new_window.show()

    def update_function_name(self, new_name):
        # Llamar al método del NavWidget para actualizar el nombre
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save_image(self):
        # muestra para seleccionar archivo, tambien lo guarda en carpeta input_files
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                   "Archivos (*.mp4 *.jpg *.png *.jpeg *mkv)")

        # Si se selecciona un archivo, se muestra su ruta en el input
        if self.file_path:
            # Call the function to send the file to the API
            self.file_path = self.file_path
            save_file = SaveFile()
            save_file.select_and_save_file(self.file_path)
            self.upper_left_area.video_path_input.setText(self.file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")


    def upload_image_path_and_save(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image File', '', 'Images (*.png *.jpg *.jpeg)')

        if file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.upper_left_area.image_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")

    

    def searchResults(self):
        word = None

        # Verifica que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún archivo.")
            return

        # Clear the rows before processing
        self.right_layout.clear_rows()

        # Process Window initialized
        self.start_process()

        endpoint = '/api/video-to-images'
        # Envía el video a la API y obtiene la respuesta
        response = send_to_ConvertService(self.file_path, endpoint)
        print (response)
        if response and response.get("download_URL"):
            # Extrae la URL de descarga de la respuesta
            zip_url = response["download_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta, el folder extraido y el nombre del zip file
            file_info = download_file(zip_url)

            # Verifica si la descarga falló
            if not file_info:
                QMessageBox.critical(self, "Error", "Error al descargar el archivo ZIP.")
                return
            
            # Guarda la información del archivo descargado en la clase
            self.downloaded_file_info = file_info  # Aquí guardamos la información para usarla en la función showImage
            word = self.upper_left_area.word_input.currentText()
            model_type = self.upper_left_area.neural_network_model_combobox.currentText()
            confidence_threshold = float(self.upper_left_area.percentage_combobox.currentText()) / 100

            if model_type != "Face Recognizer" and not word:
                QMessageBox.critical(self, "Error", "No se ha ingresado ninguna palabra.")
                return

            # Define la URL del endpoint dependiendo del tipo de modelo
            if model_type == "Gender Recognizer":
                endpoint = "/api/recognition"
                model_type_to_send = "gender"
            elif model_type == "Object Recognizer":
                endpoint = "/api/recognition"
                model_type_to_send = "object"
            elif model_type == "Face Recognizer":
                endpoint = "/api/face_recognition"
                model_type_to_send = "face recognition"
            else:
                QMessageBox.critical(self, "Error", "Modelo no válido.")
                return

            if model_type == "Face Recognizer":
                image_path = self.upper_left_area.image_path_input.text()

                if not os.path.isfile(image_path):
                    QMessageBox.critical(self, "Error", "La imagen seleccionada no existe o es inválida.")
                    return

                combined_data = {
                    "word": model_type_to_send,
                    "model_type": "object",
                    "confidence_threshold": confidence_threshold,
                    "zip_url": zip_url
                }
                # Envía los datos al servicio ML
                ml_service_response = send_file_to_MLservice(combined_data, endpoint, image_path)
            else:
                word = self.upper_left_area.word_input.currentText()  # Campo de texto para la palabra
                combined_data = {
                    "word": word,
                    "model_type": model_type_to_send,
                    "confidence_threshold": confidence_threshold,
                    "zip_url": zip_url
                }
                # Envía los datos al servicio ML
                ml_service_response = send_to_MLservice(combined_data, endpoint)
            
            print("Datos enviados al servicio ML:", combined_data)  # Para depuración
            
            if ml_service_response:
                print("ML Service Response:", ml_service_response)
                
                # Extrae los resultados de la respuesta
                results = ml_service_response.get('results', [])

                if results:  # Verificar si 'results' no está vacío
                    # Ordenar por key 'second'
                    results = sorted(results, key=lambda x: int(x['second']))
                    # Inserta cada resultado en la tabla en su respectiva columna
                    for result in results:
                        algorithm = result.get('algorithm', '')
                        percentage = result.get('percentage', 0.0)
                        second = result.get('second', '')
                        word = result.get('word', '')

                        # Tiempo
                        time = seconds_to_hms(second)

                        # Añadir valores exttraidos a la tabla
                        self.result_matrix = [algorithm, word, percentage, second, time]
                        self.showNewRow()

                    self.center_widget.hide()
                    self.right_widget.show()

                    self.process_complete()
                
                else:
                    self.process_interrupted()
                    QMessageBox.information(self, "Sin resultados", f"No se encontró {word} en el video.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo procesar los datos con el servicio ML.")
        else:
            QMessageBox.critical(self, "Error", "Error al procesar el video o no se encontró el ZIP URL.")

    def showNewRow(self):
        self.right_layout.add_new_row(self.result_matrix)
        #implementar para que pasen las filas que devuelvan


    def showData(self):
        print(self.upper_left_area.get_video_path(), self.upper_left_area.get_word(),
            self.upper_left_area.get_percentage_label(),
            self.upper_left_area.get_neural_network_model(),
            sep=os.linesep)
        
    def showImage(self):
        # Obtener la fila seleccionada
        selected_row = self.right_layout.table.currentRow()

        # Verificar si no se ha seleccionado ninguna fila
        if selected_row == -1:
            QMessageBox.critical(self, "Error", "Select a row first.")
            return

        # Verificar si se ha seleccionado toda la tabla o todas las filas
        selection_model = self.right_layout.table.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        # Calcular el número de celdas seleccionadas
        total_cells = self.right_layout.table.rowCount() * self.right_layout.table.columnCount()

        if len(selected_indexes) == total_cells:
            QMessageBox.warning(self, "Warning", "You have selected the entire table. Please select just one row.")
            return

        # Obtener el dato de la columna 4 (second) de la fila seleccionada
        image_name = self.right_layout.table.item(selected_row, 3).text() + ".jpg"

        # Construir la ruta de la imagen usando la carpeta de extracción
        file_info = self.downloaded_file_info
        image_path = os.path.join(file_info["extract_folder"], image_name)

        # Verificar si la imagen existe
        if not os.path.exists(image_path):
            print(f"No se encontró la imagen: {image_path}")
            QMessageBox.warning(self, "Advertencia", f"No se encontró la imagen: {image_path}")
            return

        # Abrir la imagen en un diálogo
        dialog = ImageDialog(image_path, self)
        dialog.exec_()

    def showInVideo(self):
        # Obtener la fila seleccionada
        selected_row = self.right_layout.table.currentRow()

        # Verificar si no se ha seleccionado ninguna fila
        if selected_row == -1:
            QMessageBox.critical(self, "Error", "Select a row first.")
            return

        # Verificar si se ha seleccionado toda la tabla o todas las filas
        selection_model = self.right_layout.table.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        # Calcular el número de celdas seleccionadas
        total_cells = self.right_layout.table.rowCount() * self.right_layout.table.columnCount()

        if len(selected_indexes) == total_cells:
            QMessageBox.warning(self, "Warning", "You have selected the entire table. Please select just one row.")
            return

        if not self.file_path:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un video primero.")
            return
        
        # Extraer el segundo desde la columna correspondiente (columna 3)
        second = int(self.right_layout.table.item(selected_row, 3).text())
        
        file_path = self.file_path
        # Crear y mostrar la ventana del reproductor de video
        self.video_player_window = VideoPlayer(file_path)

        # Mostrar la ventana del reproductor
        self.video_player_window.show()
        
        # Abrir el video en el segundo especificado
        self.video_player_window.play_video(second)


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