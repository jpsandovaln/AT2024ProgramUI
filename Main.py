import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, \
    QMessageBox
from DownLeftArea import DownLeftArea
from RigthLayout import Rigthlayout
from SaveFile import SaveFile
from UpperLeftArea import UpperLeftArea
from ImageDialog import ImageDialog
import requests


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        # Window configurations
        self.setWindowTitle('Recognizer')
        self.setGeometry(100, 100, 1000, 600)

        # Layout principal horizontal
        main_layout = QHBoxLayout()
        #self.setStyleSheet("background-color: #FFFFFF")

        # Layout principal izquierda
        left_layout = QVBoxLayout()

        # Área izquierda de labels y botones
        self.upper_left_area = UpperLeftArea()

        # Área izquierda de lista de nombres
        down_left_area = DownLeftArea()

        # Añadir áreas al layout izquierdo
        left_layout.addWidget(self.upper_left_area)
        left_layout.addWidget(down_left_area)

        # Layout derecha para la tabla
        self.right_layout = Rigthlayout()

        # Añadir los layouts de la izquierda y derecha al layout principal
        main_layout.addLayout(left_layout, 1)  # El 1 es el factor de expansión
        main_layout.addLayout(self.right_layout, 3)  # El 3 es el factor de expansión

        # Aplicar el layout principal a la ventana
        self.setLayout(main_layout)

        # Triggers
        self.upper_left_area.browse_button.clicked.connect(self.show_path_and_save_image)
        self.upper_left_area.search_button.clicked.connect(self.searchResults)
        self.right_layout.show_image_button.clicked.connect(self.showImage)


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
            QMessageBox.critical(self, "Error", "No se pudo copiar el archivo")
            print("Algo fallo al abrir el archivo, es muy probable que se presiono 'Cancelar'")

    def send_video_to_api(self, file_path):
        # Endpoint URL
        url = "http://localhost:9090/api/video-to-images"  # Replace with your actual API URL

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
        if response and response.get("download_ZIP_URL"):
            # Extrae la URL de descarga de la respuesta
            zip_url = response["download_ZIP_URL"]

            # Descarga el archivo ZIP y guarda su ruta absoluta
            zip_path = self.download_file(zip_url)

            if not zip_path:
                QMessageBox.critical(self, "Error", "Error al descargar el archivo ZIP.")
                return

            # Obtiene la palabra del campo de entrada
            word = self.upper_left_area.word_input.text()  # Campo de texto para la palabra
            model_type = self.upper_left_area.neural_network_model_combobox.currentText()
            confidence_threshold = float(self.upper_left_area.percentage_combobox.currentText()) / 100

            if not word:
                QMessageBox.critical(self, "Error", "No se ha ingresado ninguna palabra.")
                return

            # Define la URL del endpoint dependiendo del tipo de modelo
            if model_type == "Deepface":
                endpoint = "/gender_recognition"
            elif model_type == "Yolo":
                endpoint = "/object_recognition"
            else:
                QMessageBox.critical(self, "Error", "Modelo no válido.")
                return

            # Combina los datos en un objeto
            combined_data = {
                "word": word,
                "model_type": model_type,
                "confidence_threshold": confidence_threshold,
                "zip_filename": zip_path  # Enviar la ruta absoluta del ZIP
            }
            print(combined_data)

            # Envía los datos al servicio ML
            ml_service_response = self.send_to_ml_service(combined_data, endpoint)
            if ml_service_response:
                print("ML Service Response:", ml_service_response)
            else:
                QMessageBox.critical(self, "Error", "No se pudo procesar los datos con el servicio ML.")

        else:
            QMessageBox.critical(self, "Error", "Error al procesar el video o no se encontró el ZIP URL.")

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
        base_url = "http://localhost:5000"
        url = base_url + endpoint
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"ML Service Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"Exception while sending data to ML service: {e}")
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
        image_path = 'input_files/meetpoint-meetpoint.png'
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
