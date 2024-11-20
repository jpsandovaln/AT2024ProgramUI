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