# main.py

from PyQt5.QtWidgets import QApplication
from views.video_to_images import VideoToImagesView
from views.video_to_video import VideoToVideoView  # Ahora solo importamos VideoToVideoWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoToImagesView()
    window.show()
    sys.exit(app.exec_())
