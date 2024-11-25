import vlc
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox

class VideoPlayer(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.setWindowTitle("Reproductor de Video")
        self.setGeometry(100, 100, 800, 600)

        # Crear el reproductor VLC
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        self.media = self.instance.media_new(file_path)
        self.media_player.set_media(self.media)

        # Configurar ventana de video en PyQt
        self.media_player.set_hwnd(int(self.winId()))

        # Layout principal
        self.layout = QVBoxLayout(self)

        # Botones de control
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")

        self.play_button.clicked.connect(self.play)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)

        # Agregar botones al layout
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)

    def play_video(self, second=0):
        """Carga el video en el segundo indicado y lo deja pausado."""
        try:
            self.media_player.play()
            self.media_player.set_time(second * 1000)  # Establecer posición en milisegundos
            self.media_player.pause()  # Pausar inmediatamente
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo reproducir el video: {str(e)}")

    def play(self):
        """Iniciar la reproducción del video."""
        self.media_player.play()

    def pause(self):
        """Pausar el video."""
        self.media_player.pause()

    def stop(self):
        """Detener la reproducción y reiniciar la posición."""
        self.media_player.stop()


    def closeEvent(self, event):
        """Liberar recursos de VLC al cerrar."""
        self.media_player.stop()
        self.media_player.release()
        super().closeEvent(event)
