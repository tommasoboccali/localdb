from pymongo import MongoClient
from bson import json_util
from jsonschema import validate, ValidationError
import pymongo
import os
import json
from dotenv import load_dotenv
import random
from faker import Faker

fake = Faker()

# Load the schema
with open("all_schemas.json", "r") as f:
    all_schemas = json.load(f)

module_schema = all_schemas["module"]
logbook_schema = all_schemas["logbook"]
current_cabling_map_schema = all_schemas["CurrentCablingMap"]
connection_snapshot_schema = all_schemas["ConnectionSnapshot"]
tests_schema = all_schemas["tests"]

load_dotenv("mongo.env")
username = os.environ.get("MONGO_USERNAME")
password = os.environ.get("MONGO_PASSWORD")
db_name = os.environ.get("MONGO_DB_NAME")

print(f"username: {username}, password: {password}")
client = MongoClient(f"mongodb://{username}:{password}@localhost:27017")
db = client[db_name]
# we already have a database called "test" from the previous example
# db = client['test']
# we also have a collection called "modules" from the previous example
modules_collection = db["modules"]
logbook_collection = db["logbook"]
current_cabling_map_collection = db["current_cabling_map"]
connection_snapshot_collection = db["connection_snapshot"]
tests_collection = db["tests"]

# Populate modules
module_ids = []
for i in range(1000):  # Creating 100 random modules
    module = {
        "moduleID": f"M{i}",
        "position": random.choice(["lab", "field", "storage"]),
        "status": random.choice(["operational", "maintenance", "decommissioned"]),
        "overall_grade": random.choice(["A", "B", "C"])
    }
    modules_collection.insert_one(module)
    module_ids.append(module['moduleID'])

# Populate tests
for i in range(500):  # Creating 50 random tests
    test = {
        "testID": f"T{i}",
        "modules_list": random.sample(module_ids, k=random.randint(1, 10)),  # 1 to 10 modules per test
        "testType": random.choice(["Type1", "Type2", "Type3"]),
        "testDate": fake.date(),
        "testOperator": fake.name(),
        "testStatus": random.choice(["completed", "ongoing", "failed"]),
        "testResults": {"result": random.choice(["pass", "fail"])}
    }
    tests_collection.insert_one(test)