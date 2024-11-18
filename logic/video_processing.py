# manejar la lógica de procesamiento de datos
# Funciones para este archivo:

#   Manejo de datos extraídos del servicio ML, como:
#       Convertir segundos a formato HH:MM:SS: seconds_to_hms
#       Construir y procesar resultados del servicio ML.
#   Lógica de creación del objeto combined_data.

# Razón: La lógica de negocio debería estar separada de la UI para facilitar la prueba y reutilización.

def seconds_to_hms(seconds):
    if isinstance(seconds, str):
        seconds = int(seconds)  # Convierte de cadena a entero si es necesario

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"