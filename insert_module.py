from pymongo import MongoClient
import json
from jsonschema import validate, ValidationError


def insert_module(data):
    try:
        validate(instance=data, schema=schema)
        modules_collection.insert_one(data)
        print("Insert successful")
    except ValidationError as e:
        print(f"Validation error: {e}")


if __name__ == '__main__':
    client = MongoClient('mongodb://localhost:27017/')
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

    insert_module(sample_module_data)

    # print all documents in the collection
    for doc in modules_collection.find():
        print(doc)
