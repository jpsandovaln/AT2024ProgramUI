import requests
import json
import os
from singleton import app_state
from singleton.app_state import AppState

def send_to_ConvertService(file_path, endpoint):
    # Endpoint URL
    url = "http://localhost:9090" + endpoint

    # Prepare the file for the POST request
    files = {'file': open(file_path, 'rb')}
    # Access the JWT token from AppState
    token = AppState().jwt_token
    if not token:
        return None

    # Include the JWT token in the headers
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }

    try:
        # Send the request
        response = requests.post(url, files=files, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return JSON response if successful
        else:
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
    


def send_to_ConvertService_VideoToVideo(file_path, endpoint, format, fps=None, vcodec=None, acodec=None, achannel=None):
    # Endpoint URL: 
    url = "http://localhost:9090" + endpoint 
    
    # Prepare the file for the POST request
    files = {'file': open(file_path, 'rb')}

    # Prepare the additional parameters to be sent with the request
    data = {
        'format': format,
        'fps': fps,
        'vcodec': vcodec,
        'acodec': acodec,
        'achannel': achannel
    }

    try:
        # Send the request with the file and the additional parameters
        response = requests.post(url, files=files, data=data)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return JSON response if successful
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

import requests

def send_to_ConvertService_ImageToImage(file_path, endpoint, format, resize_width=None, resize_height=None, rotate_angle=None, grayscale=False, blur=False, contour=False, detail=False, edge_enhance=False, edge_enhance_more=False, emboss=False, find_edges=False, sharpen=False, smooth=False, smooth_more=False):
    url = "http://localhost:9090" + endpoint

    # Open the file in binary mode and prepare it for the POST request
    with open(file_path, 'rb') as file:
        files = {'image': file}

        # Prepare the additional parameters to be sent with the request
        data = {
            'format': format,
        }

        # Add the additional parameters dynamically based on their values
        if resize_width is not None:
            data['resize_width'] = resize_width
        if resize_height is not None:
            data['resize_height'] = resize_height
        if rotate_angle is not None:
            data['rotate'] = rotate_angle
        if grayscale:
            data['GRAYSCALE'] = grayscale
        if blur:
            data['BLUR'] = blur
        if contour:
            data['CONTOUR'] = contour
        if detail:
            data['DETAIL'] = detail
        if edge_enhance:
            data['EDGE_ENHANCE'] = edge_enhance
        if edge_enhance_more:
            data['EDGE_ENHANCE_MORE'] = edge_enhance_more
        if emboss:
            data['EMBOSS'] = emboss
        if find_edges:
            data['FIND_EDGES'] = find_edges
        if sharpen:
            data['SHARPEN'] = sharpen
        if smooth:
            data['SMOOTH'] = smooth
        if smooth_more:
            data['SMOOTH_MORE'] = smooth_more

        try:
            # Send the request with the file and the additional parameters
            response = requests.post(url, files=files, data=data)

            # Check if the request was successful
            if response.status_code == 200:
                return response.json()  # Return JSON response if successful
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None


def authenticate_user(self, username, password):
    data = {
        "username": username,
        "password": password
    }
    global jwt_token

    try:
        # We make the request to Post for authenticate the user
        response = requests.post("http://localhost:9090/api/login", json=data)

        if response.status_code == 200:
            # If success authentication, we obtain the token

            jwt_token = response.json().get("access_token")

            if jwt_token:
                AppState().jwt_token = jwt_token
                return True, jwt_token  
            else:
                return False, "Token not found"
        else:
            # If authentication fails
            return False, response.text
    except Exception as e:
        return False, str(e)
