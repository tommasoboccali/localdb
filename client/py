from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        insert_button = QPushButton('Insert')
        insert_button.clicked.connect(self.go_to_insert_screen)

        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.go_to_browse_screen)

        modify_button = QPushButton('Modify')
        modify_button.clicked.connect(self.go_to_modify_screen)

        layout.addWidget(insert_button)
        layout.addWidget(browse_button)
        layout.addWidget(modify_button)

        self.setLayout(layout)
        self.setWindowTitle('Welcome')

    def go_to_insert_screen(self):
        print('Go to Insert Screen')

    def go_to_browse_screen(self):
        print('Go to Browse Screen')

    def go_to_modify_screen(self):
        print('Go to Modify Screen')

if __name__ == '__main__':
    app = QApplication([])

    welcome_screen = WelcomeScreen()
    welcome_screen.show()

    app.exec_()
