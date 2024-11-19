def seconds_to_hms(seconds):
        if isinstance(seconds, str):
            seconds = int(seconds)  # Convierte de cadena a entero si es necesario

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        return f"{hours:02}:{minutes:02}:{seconds:02}"