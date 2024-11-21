# main.py

from PyQt5.QtWidgets import QApplication

from views.login import LoginView
import sys

jwt_token = None
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    sys.exit(app.exec_())
