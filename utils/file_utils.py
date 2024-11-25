import zipfile
import requests
import os


def download_file(url):
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

                # Define the output path for the extracted files
                extract_folder = os.path.splitext(local_filename)[0]  # Folder name without the .zip extension
                os.makedirs(extract_folder, exist_ok=True)

                # Extract the ZIP file into the specified folder
                with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder)

                print(f"Archivo descargado en: {local_filename}")
                print(f"Archivo descomprimido en: {extract_folder}")
                    
                # Return a dictionary with useful information
                return {
                    "zip_name": os.path.basename(local_filename),  # Name of the ZIP file
                    "zip_path": os.path.abspath(local_filename),  # Absolute path of the ZIP file
                    "extract_folder": os.path.abspath(extract_folder),  # Path to the extracted folder
                }
            else:
                print(f"Error al descargar el archivo. Código de estado: {response.status_code}")
                return None
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None


def download_media(url):
    try:
        # Define el nombre del archivo a partir del nombre en la URL
        local_filename = os.path.join("downloaded_files", os.path.basename(url))
        os.makedirs(os.path.dirname(local_filename), exist_ok=True)

        # Realiza la descarga del archivo
        with requests.get(url, stream=True) as r:
            if r.status_code == 200:
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"Archivo descargado en: {local_filename}")
                # Devuelve el path del archivo descargado
                return local_filename
            else:
                print(f"Error al descargar el archivo. Código de estado: {r.status_code}")
                return None
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        return None

