from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFormLayout
from PyQt5.QtCore import Qt
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv('mongo.env')
username = os.environ.get('MONGO_USERNAME')
password = os.environ.get('MONGO_PASSWORD')
db_name = os.environ.get('MONGO_DB_NAME')
client = MongoClient(f'mongodb://{username}:{password}@localhost:27017')
db = client[db_name]

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setGeometry(100, 100, 300, 200)  # x, y, width, height

        insert_button = QPushButton('Insert')
        insert_button.clicked.connect(self.go_to_insert_screen)

        browse_button = QPushButton('Browse')
        #browse_button.clicked.connect(self.go_to_browse_screen)

        modify_button = QPushButton('Modify')
        #modify_button.clicked.connect(self.go_to_modify_screen)

        connection_status_button = QPushButton('Connection Status')
        connection_status_button.setEnabled(False)
        if db:
            connection_status_button.setStyleSheet("background-color: green")
            connection_status_button.setText("Connected")

        layout.addWidget(connection_status_button)
        layout.addWidget(insert_button)
        layout.addWidget(browse_button)
        layout.addWidget(modify_button)

        self.setLayout(layout)
        self.setWindowTitle('Welcome')

    def go_to_insert_screen(self):
        self.insert_screen = InsertScreen()
        self.insert_screen.show()

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
        module_name_value = self.module_name.text()
        module_status_value = self.module_status.text()

        if module_name_value and module_status_value:
            module_data = {'name': module_name_value, 'status': module_status_value}
            db.modules.insert_one(module_data)
            print(f'Inserted {module_name_value} with status {module_status_value} into MongoDB.')
        else:
            print("Please fill all fields")

if __name__ == '__main__':
    app = QApplication([])

    welcome_screen = WelcomeScreen()
    welcome_screen.show()

    app.exec_()
