from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
from jsonschema import validate, ValidationError
import pymongo
import os
import json
from dotenv import load_dotenv
import random
from faker import Faker
import timeit

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

# at the start, empty the collections modules, logbook, current_cabling_map, tests
modules_collection.drop()
logbook_collection.drop()
current_cabling_map_collection.drop()
connection_snapshot_collection.drop()
tests_collection.drop()


# Populate modules
module_ids = []
for i in range(2000):  # Creating 100 random modules
    module = {
        "moduleID": f"M{i}",
        "position": random.choice(["lab", "field", "storage"]),
        "logbook": {"entry": "Initial setup"},
        "local_logbook": {"entry": "Local setup"},
        "ref_to_global_logbook": [],
        "status": random.choice(["operational", "maintenance", "decommissioned"]),
        "overall_grade": random.choice(["A", "B", "C"]),
        "underwent_tests": []
    }
    inserted_module = modules_collection.insert_one(module)
    module_ids.append(inserted_module.inserted_id)

# Populate tests
test_ids = []
for i in range(10000):  # Creating 50 random tests
    involved_modules = random.sample(module_ids, k=random.randint(1, 10))
    test = {
        "testID": f"T{i}",
        "modules_list": involved_modules,
        "testType": random.choice(["Type1", "Type2", "Type3"]),
        "testDate": fake.date(),
        "testOperator": fake.name(),
        "testStatus": random.choice(["completed", "ongoing", "failed"]),
        "testResults": {"result": random.choice(["pass", "fail"])}
    }
    inserted_test = tests_collection.insert_one(test)
    test_ids.append(inserted_test.inserted_id)

    # Update modules' underwent_tests field
    for module_id in involved_modules:
        modules_collection.update_one(
            {"_id": ObjectId(module_id)},
            {"$push": {"underwent_tests": inserted_test.inserted_id}}
        )

def fetch_tests_for_module():
    module_id_to_query = random.choice(module_ids)
    module_data = modules_collection.find_one({"_id": module_id_to_query})
    tests_module_underwent = tests_collection.find({"_id": {"$in": module_data.get("underwent_tests", [])}}).count()

def fetch_modules_for_test():
    test_id_to_query = random.choice(test_ids)
    test_data = tests_collection.find_one({"_id": test_id_to_query})
    modules_in_test = modules_collection.find({"_id": {"$in": test_data.get("modules_list", [])}}).count()

# Measure the time taken for fetching all tests for a random module
time_for_fetching_tests = timeit.timeit(fetch_tests_for_module, number=100)
print(f"Time taken for fetching all tests for a module over 100 iterations: {time_for_fetching_tests} seconds")

# Measure the time taken for fetching all modules for a random test
time_for_fetching_modules = timeit.timeit(fetch_modules_for_test, number=100)
print(f"Time taken for fetching all modules for a test over 100 iterations: {time_for_fetching_modules} seconds")

# print 10 random entries to show that the database is populated
# print("Modules:")
# for module in modules_collection.aggregate([{"$sample": {"size": 10}}]):
#     print(json.dumps(module, indent=2, default=json_util.default))

# print("Tests:")
# for test in tests_collection.aggregate([{"$sample": {"size": 10}}]):
#     print(json.dumps(test, indent=2, default=json_util.default))
