import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, \
    QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from components.HeaderWidget import HeaderWidget
from components.NavWidget import NavWidget
from components.UpperLeftArea import UpperLeftArea
from components.DownLeftArea import DownLeftArea
from components.RigthLayout import Rigthlayout
from components.CenterLayout import CenterLayout
from SaveFile import SaveFile
from ImageDialog import ImageDialog
import requests
import json


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

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
        nav_widget = NavWidget()
        overall_layout.addWidget(nav_widget)

        # Main Horizontal Layout 
        main_layout = QHBoxLayout()

        # Main left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 80)
        
        # Left area of labels and buttons
        self.upper_left_area = UpperLeftArea()
        
        # Left area with names list
        self.down_left_area = DownLeftArea()
        
        # Add areas into left layout
        left_layout.addWidget(self.upper_left_area)
        left_layout.addWidget(self.down_left_area)

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
        self.down_left_area.browse_image_button.clicked.connect(self.upload_image_path_and_save)
        self.upper_left_area.neural_network_model_combobox.currentIndexChanged.connect(self.update_down_left_model)


    def update_down_left_model(self):
        selected_model = self.upper_left_area.get_neural_network_model()
        self.down_left_area.set_model(selected_model)
        # if selected_model == 'Face Recognizer':
        #     self.down_left_area.show()  # Mostrar el DownLeftArea
        #     self.upper_left_area.word_label.show()  # Mostrar el word_label
        #     self.upper_left_area.word_input.show()  # Mostrar el word_input
        # else:
        #     self.down_left_area.hide()  # Ocultar el DownLeftArea
        #     self.upper_left_area.word_label.hide()  # Ocultar el word_label
        #     self.upper_left_area.word_input.hide()  # Ocultar el word_input

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

    def send_video_to_api(self, file_path):
        # Endpoint URL
        url = "http://localhost:9090/api/video-to-images" 

        # Prepare the file for the POST request
        files = {'file': open(file_path, 'rb')}

        try:
            # Send the request
            response = requests.post(url, files=files)
            print(response)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()  # Return JSON response if successful
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def searchResults(self):
        # Verifica que se haya seleccionado un archivo
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No se ha seleccionado ningún archivo.")
            return

        # Envía el video a la API y obtiene la respuesta
        response = self.send_video_to_api(self.file_path)
        if response and response.get("download_URL"):
            # Extrae la URL de descarga de la respuesta
            zip_url = response["download_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta
            zip_path = self.download_file(zip_url)
            if not zip_path:
                QMessageBox.critical(self, "Error", "Error al descargar el archivo ZIP.")
                return

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

                # Inserta cada resultado en la tabla en su respectiva columna
                for result in results:
                    algorithm = result.get('algorithm', '')
                    path = result.get('path', '')
                    percentage = result.get('percentage', 0.0)
                    second = result.get('second', '')
                    word = result.get('word', '')

                    # Tiempo
                    time = self.seconds_to_hms(second)

                    # Añadir valores exttraidos a la tabla
                    self.result_matrix = [algorithm, word, percentage, second, time]
                    self.showNewRow()
            else:
                QMessageBox.critical(self, "Error", "No se pudo procesar los datos con el servicio ML.")
        else:
            QMessageBox.critical(self, "Error", "Error al procesar el video o no se encontró el ZIP URL.")

        self.center_widget.hide()
        self.right_widget.show()

    def seconds_to_hms(self, seconds):
        if isinstance(seconds, str):
            seconds = int(seconds)  # Convierte de cadena a entero si es necesario

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def download_file(self, url):
        try:
            # Define the output path for the downloaded file
            local_filename = os.path.join("downloaded_files", os.path.basename(url))
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)

            # Download the file
            with requests.get(url, stream=True) as response:
                if response.status_code == 200:
                    with open(local_filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return os.path.abspath(local_filename)  # Return the absolute path
                else:
                    print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
                    return None
        except Exception as e:
            print(f"Error al descargar el archivo: {e}")
            return None

    def send_to_ml_service(self, data, endpoint):
        # URL base del servicio ML
        base_url = "http://localhost:5001"
        url = base_url + endpoint
        
        # Agrega el encabezado Content-Type explícitamente (opcional)
        headers = {'Content-Type': 'application/json'}
        
        try:
            # Envía el diccionario como JSON
            response = requests.post(url, json=data, headers=headers)
            
            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                return response.json()
            else:
                # Muestra el mensaje de error detallado en caso de falla
                print(f"Error al procesar los datos en el servicio ML: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error al enviar datos al servicio ML: {e}")
            return None

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

        if selected_row == -1:
            print("Por favor, selecciona una fila primero.")
            return

        # Ruta de imagen hardcodeada, implementar para pasar
        #image_path = self.right_layout.table.item(selected_row, 5).text()
        image_path = 'input_files/yingYang.jpeg'
        # Abrir la imagen en un diálogo
        dialog = ImageDialog(image_path, self)
        dialog.exec_()

    def getResult(self):
        #Me deberia devolver el resultado, esto se pondra en las filas
        return['1','2','3','4','5']


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())