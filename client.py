from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QFormLayout, QLineEdit
# New Insert Screen Class
class InsertScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
        
        self.module_name = QLineEdit()
        self.module_status = QLineEdit()
        
        layout.addRow('Module Name:', self.module_name)
        layout.addRow('Module Status:', self.module_status)
        
        insert_button = QPushButton('Insert into DB')
        insert_button.clicked.connect(self.insert_into_db)
        
        layout.addRow(insert_button)
        
        self.setLayout(layout)
        self.setWindowTitle('Insert Screen')

    def insert_into_db(self):
        # Logic to insert into MongoDB
        module_name_value = self.module_name.text()
        module_status_value = self.module_status.text()
        
        print(f'Inserting {module_name_value} with status {module_status_value} into MongoDB.')

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
        self.insert_screen = InsertScreen()
        self.insert_screen.show()

    def go_to_browse_screen(self):
        print('Go to Browse Screen')

    def go_to_modify_screen(self):
        print('Go to Modify Screen')

if __name__ == '__main__':
    app = QApplication([])

    welcome_screen = WelcomeScreen()
    welcome_screen.show()

    app.exec_()
