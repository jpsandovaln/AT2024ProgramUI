from PyQt5.QtWidgets import QMessageBox, QProgressDialog
from PyQt5.QtCore import Qt


def start_process(self):
    # Crea el cuadro de diálogo "Procesando"
    self.progress_dialog = QProgressDialog("Procesando, por favor espere...", None, 0, 0, self)
    self.progress_dialog.setWindowModality(Qt.ApplicationModal)
    self.progress_dialog.setCancelButtonText(None)
    self.progress_dialog.setWindowTitle("Procesando")
    self.progress_dialog.setRange(0, 0)  # Indeterminado
    self.progress_dialog.show()
    
def process_interrupted(self):
    # Interrumpe proceso y cierra cuadro de diálogo
    self.process_dialog.close()

def process_complete(self):
    # Cierra el cuadro de diálogo
    self.progress_dialog.close()
    QMessageBox.information(self, "Completado", "El proceso ha finalizado con éxito.")