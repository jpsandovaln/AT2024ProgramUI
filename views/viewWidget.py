import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea import UpperLeftArea
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from utils.SaveFile import SaveFile


class ViewWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        from views.video_to_video import VideoToVideoView

        # Window configurations
        self.setWindowTitle('JalaRecognizer')
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
        # self.nav_widget.left_arrow_clicked.connect(self.open_right_window)
        # self.nav_widget.right_arrow_clicked.connect(self.open_right_window)

        # self.update_function_name('Video Frame Analyzer')

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
            # label_text="Upload your video and select the object, face, or person (male or female) you want to search for. Using Machine Learning, the system analyzes each frame of the video and provides a list of results where the selected object, face, or person is detected, helping you find exactly what you're looking for in the video."
            label_text=""
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
        self.upper_left_area.browse_image_button.clicked.connect(self.upload_image_path_and_save)


    def open_right_window(self):
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_video import VideoToVideoWindow

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = VideoToVideoWindow()
        self.new_window.show()

    def open_left_window(self):
        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_video import VideoToVideoWindow

        # Cerrar la ventana principal
        self.close()

        # Crear y mostrar la nueva ventana
        self.new_window = VideoToVideoWindow()
        self.new_window.show()

    def update_function_name(self, new_name):
        # Llamar al método del NavWidget para actualizar el nombre
        self.nav_widget.update_feature_name(new_name)

    def show_path_and_save_image(self):
        # muestra para seleccionar archivo, tambien lo guarda en carpeta input_files
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                   "Archivos (*.mp4 *.jpg *.png *.jpeg *mkv)")
        # Si se selecciona un archivo, se muestra su ruta en el input
        if file_path:
            # Call the function to send the file to the API
            self.file_path = file_path
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.upper_left_area.video_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")


    def upload_image_path_and_save(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image File', '', 'Images (*.png *.jpg *.jpeg)')
        if file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.down_left_area.image_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")

   

    def searchResults(self):
        # Verifica que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún archivo.")
            return

        # Process Window initialized
        self.start_process()

        # Envía el video a la API y obtiene la respuesta
        response = self.send_video_to_api(self.file_path)
        print ( response)
        if response and response.get("download_URL"):
            # Extrae la URL de descarga de la respuesta
            zip_url = response["download_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta, el folder extraido y el nombre del zip file
            file_info = self.download_file(zip_url)

            # Verifica si la descarga falló
            if not file_info:
                QMessageBox.critical(self, "Error", "Error al descargar el archivo ZIP.")
                return
            
            # Guarda la información del archivo descargado en la clase
            self.downloaded_file_info = file_info  # Aquí guardamos la información para usarla en la función showImage

            # Obtiene la palabra del campo de entrada
            word = self.upper_left_area.word_input.currentText()  # Campo de texto para la palabra
            model_type = self.upper_left_area.neural_network_model_combobox.currentText()
            confidence_threshold = float(self.upper_left_area.percentage_combobox.currentText()) / 100

            if not word:
                QMessageBox.critical(self, "Error", "No se ha ingresado ninguna palabra.")
                return

            # Define la URL del endpoint dependiendo del tipo de modelo
            if model_type == "Gender Recognizer":
                endpoint = "/api/recognition"
                model_type_to_send = "gender"
            elif model_type == "Object Recognizer":
                endpoint = "/api/recognition"
                model_type_to_send = "object"
            else:
                QMessageBox.critical(self, "Error", "Modelo no válido.")
                return

            # Combina los datos en un objeto
            combined_data = {
                "word": word,
                "model_type": model_type_to_send,
                "confidence_threshold": confidence_threshold,
                "zip_url": zip_url
            }
            print("Datos enviados al servicio ML:", combined_data)  # Para depuración

            # Envía los datos al servicio ML
            ml_service_response = self.send_to_ml_service(combined_data, endpoint)
            if ml_service_response:
                print("ML Service Response:", ml_service_response)
                
                # Extrae los resultados de la respuesta
                results = ml_service_response.get('results', [])

                if results:  # Verificar si 'results' no está vacío

                    # Inserta cada resultado en la tabla en su respectiva columna
                    for result in results:
                        algorithm = result.get('algorithm', '')
                        path = result.get('path', '')
                        percentage = result.get('percentage', 0.0)
                        second = result.get('second', '')
                        word = result.get('word', '')

                        # Tiempo
                        # time = self.seconds_to_hms(second)
                        time = second

                        # Añadir valores exttraidos a la tabla
                        self.result_matrix = [algorithm, word, percentage, second, time]
                        self.showNewRow()

                    self.center_widget.hide()
                    self.right_widget.show()

                    self.process_complete()
                
                else:
                    self.process_interrupted
                    QMessageBox.information(self, "Sin resultados", f"No se encontró {word} en el video.")
            else:
                QMessageBox.critical(self, "Error", "No se pudo procesar los datos con el servicio ML.")
        else:
            QMessageBox.critical(self, "Error", "Error al procesar el video o no se encontró el ZIP URL.")


    

    
    
    