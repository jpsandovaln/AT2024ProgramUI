import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, \
    QMessageBox
from DownLeftArea import DownLeftArea
from RigthLayout import Rigthlayout
from SaveFile import SaveFile
from UpperLeftArea import UpperLeftArea
from ImageDialog import ImageDialog
from HeaderWidget import HeaderWidget
import requests



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None

        # Window configurations
        self.setWindowTitle('Recognizer')
        self.setGeometry(100, 100, 1000, 700)

        # Layout to integrate header and main_layout
        overall_layout = QVBoxLayout()
    
        # Header widget in the top side
        header_widget = HeaderWidget("./logo.png")
        overall_layout.addWidget(header_widget)

        # Main Horizontal Layout 
        main_layout = QHBoxLayout()

        # Main left Layout
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0,0,0,80)
        
        # Left area of labels and buttons
        self.upper_left_area = UpperLeftArea()
        
        # Left area with names list
        self.down_left_area = DownLeftArea()
        
        # Add areas into left layout
        left_layout.addWidget(self.upper_left_area)
        left_layout.addWidget(self.down_left_area)

        # Right layout with the table
        self.right_layout = Rigthlayout()

        # Add left and right layouts into the main layout
        main_layout.addLayout(left_layout, 1)  #  1 is the expansion factor 
        main_layout.addLayout(self.right_layout, 3)  # 3 is the expansion factor 

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

    #Update down left model after change
    def update_down_left_model(self):
        selected_model = self.upper_left_area.get_neural_network_model()
        self.down_left_area.set_model(selected_model)

    #Shows path of the selected file
    def show_path_and_save_image(self):
        # sample to select file, also saves to input_files folder
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "",
                                                   "Files (*.mp4 *.jpg *.png *.jpeg *mkv)")

        # If a file is selected it path shows in the input field
        if file_path:
            # Call the function to send the file to the API
            self.file_path = file_path
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.upper_left_area.video_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Something failed opening the file, most likely 'Cancel' button was pressed.")

    #Upload file and  save it in the project directory
    def upload_image_path_and_save(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image File', '', 'Images (*.png *.jpg *.jpeg)')

        if file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.down_left_area.image_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "The file could not be copied")
            print("Something failed opening the file, most likely 'Cancel' button was pressed.")

    #Sends the selected video to converter api
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
    #Function that triggers the flow to converter and machine learning api
    def searchResults(self):
        # Verifies that a file was selected
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No file selected")
            return

        # Send video to converter api and obtains the response
        response = self.send_video_to_api(self.file_path)
        if response and response.get("download_ZIP_URL"):
            # Extract the download url from the response
            zip_url = response["download_ZIP_URL"]

            # Downloads the zip file and save the absolute path
            zip_path = self.download_file(zip_url)

            if not zip_path:
                QMessageBox.critical(self, "Error", "Error al descargar el archivo ZIP.")
                return

            # Obtains the word from the input
            word = self.upper_left_area.word_input.text()  # Text field to word
            model_type = self.upper_left_area.neural_network_model_combobox.currentText()
            confidence_threshold = float(self.upper_left_area.percentage_combobox.currentText()) / 100

            if not word:
                QMessageBox.critical(self, "Error", "No word inserted")
                return

            # Defines the url depending of the model selected
            if model_type == "Gender Recognizer":
                endpoint = "/gender_recognition"
            elif model_type == "Object Recognizer":
                endpoint = "/object_recognition"
            else:
                QMessageBox.critical(self, "Error", "Not valid model.")
                return

            # Combines data in an object
            combined_data = {
                "word": word,
                "model_type": model_type,
                "confidence_threshold": confidence_threshold,
                "zip_filename": zip_path  # Send absolute path
            }
            print(combined_data)

            # Send data to Machine Learning service
            ml_service_response = self.send_to_ml_service(combined_data, endpoint)
            if ml_service_response:
                print("ML Service Response:", ml_service_response)
            else:
                QMessageBox.critical(self, "Error", "The data could not be processed with the ML service.")

        else:
            QMessageBox.critical(self, "Error", "Error processing video or ZIP URL not found.")

    #Downloads file from the obtained url
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
                    print(f"Error downloading file. Status code: {response.status_code}")
                    return None
        except Exception as e:
            print(f"Error downloading the file: {e}")
            return None

    #Sends combined data to Machine Learning service
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
    #Shows new row with data
    def showNewRow(self):
        self.right_layout.add_new_row(self.result_matrix)
        #Implement to show the obtained data

    #Shows the data in the columns
    def showData(self):
        print(self.upper_left_area.get_video_path(), self.upper_left_area.get_word(),
              self.upper_left_area.get_percentage_label(),
              self.upper_left_area.get_neural_network_model(),
              sep=os.linesep)

    #Shows the image of the selected row
    def showImage(self):
        # Obtain the selected row
        selected_row = self.right_layout.table.currentRow()

        if selected_row == -1:
            print("Por favor, selecciona una fila primero.")
            return

        # Hardcoded image, implements
        #image_path = self.right_layout.table.item(selected_row, 5).text()
        image_path = 'input_files/yingYang.jpeg'
        # Abrir la imagen en un diálogo
        dialog = ImageDialog(image_path, self)
        dialog.exec_()

    #Obtain the result to show in the row
    def getResult(self):
        #Me deberia devolver el resultado, esto se pondra en las filas
        return['1','2','3','4','5']


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
