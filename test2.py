from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QProgressDialog, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time  # Simula el proceso pesado

class WorkerThread(QThread):
    process_complete = pyqtSignal()  # Señal que indica que el proceso terminó

    def run(self):
        # Simula un proceso pesado
        for i in range(5):  # 5 pasos, por ejemplo
            time.sleep(1)  # Simula trabajo
        self.process_complete.emit()  # Emite señal cuando el trabajo termina

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
        # Crea el cuadro de diálogo "Procesando"
        self.progress_dialog = QProgressDialog("Procesando, por favor espere...", None, 0, 0, self)
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButtonText(None)
        self.progress_dialog.setWindowTitle("Procesando")
        self.progress_dialog.setRange(0, 0)  # Indeterminado
        self.progress_dialog.show()

        # Inicia el hilo para el proceso pesado
        self.worker_thread = WorkerThread()
        self.worker_thread.process_complete.connect(self.on_process_complete)
        self.worker_thread.start()

    def on_process_complete(self):
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
