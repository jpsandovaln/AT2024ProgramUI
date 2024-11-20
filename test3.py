from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana principal")
        self.setGeometry(100, 100, 400, 300)

        # Botón para iniciar el proceso
        self.button = QPushButton("Iniciar Proceso", self)
        self.button.clicked.connect(self.start_process)
        self.button.setGeometry(100, 100, 200, 40)

    def start_process(self):
        # Crea el cuadro de diálogo "Procesando" con barra de progreso
        self.progress_dialog = QProgressDialog("Procesando, por favor espere...", None, 0, 100, self)
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButtonText(None)
        self.progress_dialog.setWindowTitle("Procesando")
        self.progress_dialog.setValue(0)  # Inicia la barra en 0
        self.progress_dialog.show()

        # Simula un proceso largo con QTimer
        self.process_steps = 0  # Contador de pasos
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.simulate_long_process)
        self.progress_timer.start(100)  # Ejecuta cada 100 ms (0.1 segundos)

    def simulate_long_process(self):
        # Simula el avance del proceso
        self.process_steps += 1
        self.progress_dialog.setValue(self.process_steps)

        if self.process_steps >= 100:  # Cuando llegue al 100% detiene el timer
            self.progress_timer.stop()
            self.process_complete()

    def process_complete(self):
        # Cierra el cuadro de diálogo
        self.progress_dialog.close()
        QMessageBox.information(self, "Completado", "El proceso ha finalizado con éxito.")

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
