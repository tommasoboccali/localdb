from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError
from dotenv import load_dotenv
import os

username = os.environ.get('MONGO_USERNAME')
password = os.environ.get('MONGO_PASSWORD')

def insert_module(data, schema=None):
    try:
        validate(instance=data, schema=schema)
        modules_collection.insert_one(data)
        print("Insert successful")
    except ValidationError as e:
        print(f"Validation error: {e}")


if __name__ == '__main__':
    client = MongoClient(f'mongodb://{username}:{password}@localhost:27017')
    db = client['test_db']

    modules_collection = db['modules']
    with open('module_schema.json', 'r') as f:
        module_schema = json.load(f)

    # Sample data
    sample_module_data = {
        "inventory": "PS_40_05_IPG-00002TEST",
        "position": "cleanroom",
        "logbook": {},
        "local_logbook": {},
        "ref_to_global_logbook": [],
        "status": "readyformount",
        "overall_grade": "A"
    }

    insert_module(sample_module_data, module_schema)

    # print all documents in the collection
    for doc in modules_collection.find():
        print(doc)
