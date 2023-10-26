from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFormLayout
from PyQt5.QtCore import Qt
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from jsonschema import validate, ValidationError
import json


load_dotenv('mongo.env')
username = os.environ.get('MONGO_USERNAME')
password = os.environ.get('MONGO_PASSWORD')
db_name = os.environ.get('MONGO_DB_NAME')
client = MongoClient(f'mongodb://{username}:{password}@localhost:27017')
db = client[db_name]

# Load the schema
with open("module_schema.json", "r") as f:
    module_schema = json.load(f)

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
        else:
            connection_status_button.setStyleSheet("background-color: red")
            connection_status_button.setText("Not Connected")

        layout.addWidget(connection_status_button)
        layout.addWidget(insert_button)
        layout.addWidget(browse_button)
        layout.addWidget(modify_button)

        self.setLayout(layout)
        self.setWindowTitle('Welcome to the Module Database!')

    def go_to_insert_screen(self):
        self.insert_screen = InsertScreen()
        self.insert_screen.show()

class InsertScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()

        self.inventory = QLineEdit()
        self.position = QLineEdit()
        self.status = QLineEdit()
        self.overall_grade = QLineEdit()
        # Add more fields based on your schema

        layout.addRow('Inventory:', self.inventory)
        layout.addRow('Position:', self.position)
        layout.addRow('Status:', self.status)
        layout.addRow('Overall Grade:', self.overall_grade)
        # Add more fields based on your schema

        insert_button = QPushButton('Insert into DB')
        insert_button.clicked.connect(self.insert_into_db)

        layout.addRow(insert_button)

        self.setLayout(layout)
        self.setWindowTitle('Insert Screen')

    def insert_into_db(self):
        data_to_insert = {
            'inventory': self.inventory.text(),
            'position': self.position.text(),
            'status': self.status.text(),
            'overall_grade': self.overall_grade.text()
            # Add more fields based on your schema
        }

        try:
            # Validate the data against the schema
            validate(instance=data_to_insert, schema=module_schema)

            # If validation succeeds, insert into MongoDB
            db.modules.insert_one(data_to_insert)
            print(f"Inserted data into MongoDB: {data_to_insert}")

        except ValidationError as e:
            print(f"Validation Error: {e.message}")

if __name__ == '__main__':
    app = QApplication([])

    welcome_screen = WelcomeScreen()
    welcome_screen.show()

    app.exec_()
