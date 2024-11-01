import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QFileDialog, \
    QMessageBox
from DownLeftArea import DownLeftArea
from RigthLayout import Rigthlayout
from SaveFile import SaveFile
from UpperLeftArea import UpperLeftArea
from ImageDialog import ImageDialog


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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
        # muestra para seleccionar archivo, tambi[en lo guarda en carpeta input_files
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                   "Archivos (*.mp4 *.jpg *.png *.jpeg *mkv)")

        # Si se selecciona un archivo, se muestra su ruta en el input
        if file_path:
            save_file = SaveFile()
            save_file.select_and_save_file(file_path)
            self.upper_left_area.video_path_input.setText(file_path)
        else:
            QMessageBox.critical(self, "Error", "No se pudo copiar el archivo")
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
