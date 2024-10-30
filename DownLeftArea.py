from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget


class DownLeftArea(QWidget):
    def __init__(self):
        super().__init__()
        self.create_down_left_area()

    def create_down_left_area(self):
        down_left_layout = QVBoxLayout()
        self.setStyleSheet(
            "background-color: #D3D3D3; border: 1px solid black;")  # Color plomo suave con borde naranja
        # Add list of names
        name_list = QListWidget()
        names = ['Joel', 'Diego', 'Jessica', 'Daria', 'Michelle', 'Rhem',
                 'Joanna', 'Paolo', 'Dayne', 'Josemar', 'Arturo']
        name_list.addItems(names)
        down_left_layout.addWidget(name_list)

        # Add layout to widget
        self.setLayout(down_left_layout)
