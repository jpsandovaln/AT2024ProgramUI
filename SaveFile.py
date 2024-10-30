import os
import shutil


class SaveFile():
    def __init__(self):
        super().__init__()
        # Crear la carpeta de destino si no existe
        self.download_folder = os.path.join(os.getcwd(), "input_files")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    # Función para seleccionar y guardar el archivo
    def select_and_save_file(self, file_path):
        # Nombre del archivo original
        file_name = os.path.basename(file_path)
        # Ruta destino en la carpeta 'archivos_descargados'
        destination_path = os.path.join(self.download_folder, file_name)
        # Copiar el archivo a la carpeta de destino
        shutil.copy(file_path, destination_path)

        """    except Exception as e:
                #QMessageBox.critical(self, "Error", f"No se pudo copiar el archivo: {e}")
                print("Algo fallo al abrir el archivo")"""
