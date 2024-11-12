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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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


    def update_down_left_model(self):
        selected_model = self.upper_left_area.get_neural_network_model()
        self.down_left_area.set_model(selected_model)

    def show_path_and_save_image(self):
        # muestra para seleccionar archivo, tambi[en lo guarda en carpeta input_files
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                   "Archivos (*.mp4 *.jpg *.png *.jpeg *mkv)")

        # Si se selecciona un archivo, se muestra su ruta en el input
        if file_path:
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
        #muestra la data que esta siendo enviada por consola
        self.showData()
        #falta decir a que clase enviara la data
        #metodo getResult esta hardcodeado, debe de devolverme el resultado de la integracion con otras clases
        self.result_matrix=self.getResult()
        #metodo que muestra la nueva fila
        self.showNewRow()

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
