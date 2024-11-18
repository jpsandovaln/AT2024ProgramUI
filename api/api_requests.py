import requests
import json
import os

def send_to_ConvertService(file_path, endpoint):
    # Endpoint URL
    url = "http://localhost:9090" + endpoint

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


def send_file_to_MLservice(data, endpoint, file_path=None):
    # URL base del servicio ML
    url = "http://localhost:5001" + endpoint

    files = None
    # Si se pasó una ruta de archivo, prepara el archivo
    if file_path:
        if not os.path.isfile(file_path):
            print("La imagen seleccionada no existe o es inválida.")
            return None
        files = {'image_file_reference': open(file_path, 'rb')}
    
    # Si 'data' ya contiene un diccionario con los parámetros necesarios, no lo envolvemos en json.dumps aquí.
    try:
        # Envía la solicitud POST con los archivos y datos (si existe el archivo)
        if files:
            response = requests.post(url, files=files, data=data)  # No envolvemos los datos en JSON aquí
        else:
            response = requests.post(url, data=data)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al procesar los datos en el servicio ML: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error al enviar datos al servicio ML: {e}")
        return None
    finally:
        # Si se abrió un archivo, cerramos el archivo después de enviarlo
        if files:
            files['image_file_reference'].close()

def send_to_MLservice(data, endpoint):
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