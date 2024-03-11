import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Main Window')
        layout.addWidget(self.label)

        self.button_open_second_window = QPushButton('Open Second Window')
        self.button_open_second_window.clicked.connect(self.open_second_window)
        layout.addWidget(self.button_open_second_window)

        self.setLayout(layout)

    def open_second_window(self):
        self.second_window = SecondWindow(self)
        self.second_window.show()
        self.hide()

class SecondWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.setWindowTitle('Second Window')
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Second Window')
        layout.addWidget(self.label)

        self.button_back_to_main = QPushButton('Back to Main Window')
        self.button_back_to_main.clicked.connect(self.back_to_main_window)
        layout.addWidget(self.button_back_to_main)

        self.setLayout(layout)
        self.main_window = main_window

    def back_to_main_window(self):
        self.main_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
