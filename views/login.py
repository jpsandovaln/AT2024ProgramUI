from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from api.api_requests import authenticate_user
from singleton import app_state
from singleton.app_state import AppState


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        app_state = AppState()
        self.create_upper_left_area()

    def create_upper_left_area(self):

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #f0f0f0;")


        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(15)
        main_layout.setAlignment(Qt.AlignCenter)


        self.label = QLabel("Welcome! Please log in:")
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
        self.label.setAlignment(Qt.AlignCenter)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(
            "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
        )

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        #self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
        )

        # Log in button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8c;
            }
            """
        )
        #Sign in without loggin in button
        self.signin_button = QPushButton("Sign in without logging in")
        self.signin_button.clicked.connect(self.open_window)
        self.signin_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton:pressed {
                background-color: #003f8c;
            }
            """
        )

        # Add widgets to layout
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)
        main_layout.addWidget(self.login_button)
        main_layout.addWidget(self.signin_button)

        self.setLayout(main_layout)

    def handle_login(self):
        # Obtain the data from the input fields
        username = self.username_input.text()
        password = self.password_input.text()


        success, token = authenticate_user(self, username, password)

        if success:
            app_state.jwt_token = token

            self.show_message("Login Successful", "You have logged in successfully!", QMessageBox.Information)
            self.close()
            from views.video_to_images import VideoToImagesView

            self.new_window = VideoToImagesView()
            self.new_window.show()
        else:
            self.show_message("Login Failed", f"Error: {token}", QMessageBox.Critical)
    def open_window(self):
        # Cerrar la ventana principal
        self.close()

        # Importar VideoToVideoWindow solo cuando sea necesario
        from views.video_to_images import VideoToImagesView

        # Create and show new window
        self.new_window = VideoToImagesView()
        self.new_window.show()

    def show_message(self, title, message, icon_type):
        # Show message box with the result
        msg_box = QMessageBox()
        msg_box.setIcon(icon_type)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    login_view = LoginView()
    login_view.show()
    sys.exit(app.exec_())
