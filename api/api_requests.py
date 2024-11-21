import requests
import json
import os
from singleton import app_state
from singleton.app_state import AppState

def send_to_ConvertService(file_path, endpoint):
    # Endpoint URL
    url = "http://localhost:9090" + endpoint

    # Verifica si el archivo existe
    if not os.path.isfile(file_path):
        return {"error": "El archivo especificado no existe."}

    # Prepara el archivo para la solicitud POST
    files = {'file': open(file_path, 'rb')}
    
    # Accede al token JWT desde AppState
    token = AppState().jwt_token
    if not token:
        return {"error": "Usuario no autenticado. Para poder utilizar este microservicio, inicie sesión por favor."}

    # Incluye el token JWT en los headers
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        # Envía la solicitud
        response = requests.post(url, files=files, headers=headers)

        # Verifica el código de respuesta
        if response.status_code == 200:
            return response.json()  # Devuelve la respuesta en JSON si es exitosa
        elif response.status_code == 401:
            return {"error": "Usuario no autenticado. Token JWT inválido o expirado."}
        else:
            return {"error": f"Error en la API: {response.status_code}"}
    except Exception as e:
        print(f"Excepción: {e}")
        return {"error": f"Excepción al procesar la solicitud: {e}"}



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

def send_to_ConvertService_ImageToImage(file_path, endpoint, format, resize_type=None, resize_width=None, resize_height=None, rotate_angle=None, grayscale=False, blur=False, contour=False, detail=False, edge_enhance=False, edge_enhance_more=False, emboss=False, find_edges=False, sharpen=False, smooth=False, smooth_more=False):
    url = "http://localhost:9090" + endpoint

    # Open the file in binary mode and prepare it for the POST request
    with open(file_path, 'rb') as file:
        files = {'image': file}

        # Prepare the additional parameters to be sent with the request
        data = {
            'output_format': format,
        }

        # Add the additional parameters dynamically based on their values
        if resize_type is not None:
            data['resize_type'] = resize_type
        if resize_width is not None:
            data['resize_width'] = resize_width
        if resize_height is not None:
            data['resize_height'] = resize_height
        if rotate_angle is not None:
            data['rotate'] = rotate_angle

        filters = []
        if grayscale:
            filters.append('GRAYSCALE')
        if blur:
            filters.append('BLUR')
        if contour:
            filters.append('CONTOUR')
        if detail:
            filters.append('DETAIL')
        if edge_enhance:
            filters.append('EDGE_ENHANCE')
        if edge_enhance_more:
            filters.append('EDGE_ENHANCE_MORE')
        if emboss:
            filters.append('EMBOSS')
        if find_edges:
            filters.append('FIND_EDGES')
        if sharpen:
            filters.append('SHARPEN')
        if smooth:
            filters.append('SMOOTH')
        if smooth_more:
            filters.append('SMOOTH_MORE')

        if filters:  # Solo agrega 'filter' si hay filtros seleccionados
            data['filter'] = filters

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

def send_to_ConvertService_AudioToAudio(file_path, endpoint, format, bitrate=None, channels=None, samplerate=None, volume=None, languagechannel=None, speed=None):
    url = "http://localhost:9090" + endpoint

    # Open the file in binary mode and prepare it for the POST request
    with open(file_path, 'rb') as file:
        files = {'audio': file}

        # Prepare the additional parameters to be sent with the request
        data = {
            'output_format': format,
        }

        # Add the additional parameters dynamically based on their values
        if bitrate is not None:
            data['bitrate'] = bitrate
        if channels is not None:
            data['channels'] = channels
        if samplerate is not None:
            data['samplerate'] = samplerate
        if volume is not None:
            data['volume'] = volume
        if languagechannel is not None:
            data['languagechannel'] = languagechannel
        if speed is not None:
            data['speed'] = speed

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
        

def send_to_ConvertService_GetMetadata(file_path, endpoint):
    # Endpoint URL: 
    url = "http://localhost:9090" + endpoint 
    
    # Prepare the file for the POST request
    files = {'file': open(file_path, 'rb')}

    try:
        # Send the request with the file and the additional parameters
        response = requests.post(url, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return JSON response if successful
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None
