from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from jsonschema import validate, ValidationError
import pymongo
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

# Load the schema
with open("module_schema.json", "r") as f:
    schema = json.load(f)


with open("logbook_schema.json", "r") as f:
    logbook_schema = json.load(f)

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
# modules_collection = db['modules']
logbook_collection = db["logbook"]


class ModulesResource(Resource):
    """Flask RESTful Resource for modules

    Args:
        Resource (Resource): Flask RESTful Resource
    """

    def get(self, inventory=None):
        """
        Retrieves a module from the database based on its inventory number, or retrieves all modules if no inventory number is provided.

        Args:
            inventory (int, optional): The inventory number of the module to retrieve. Defaults to None.

        Returns:
            If inventory is provided, returns a JSON representation of the module. If inventory is not provided, returns a JSON representation of all modules in the database.
        """
        if inventory:
            module = db.modules.find_one({"inventory": inventory})
            if module:
                return jsonify(module)
            else:
                return {"message": "Module not found"}, 404
        else:
            modules = list(db.modules.find())
            return jsonify(modules)

    def post(self):
        try:
            new_module = request.get_json()
            validate(instance=new_module, schema=schema)
            db.modules.insert_one(new_module)
            return {"message": "Module inserted"}, 201
        except ValidationError as e:
            return {"message": str(e)}, 400

    def put(self, inventory):
        updated_data = request.get_json()
        db.modules.update_one({"inventory": inventory}, {"$set": updated_data})
        return {"message": "Module updated"}, 200

    def delete(self, inventory):
        db.modules.delete_one({"inventory": inventory})
        return {"message": "Module deleted"}, 200


# API Routes
api.add_resource(ModulesResource, "/modules", "/modules/<string:inventory>")


class LogbookResource(Resource):
    def get(self, timestamp=None):
        if timestamp:
            log = logbook_collection.find_one({"timestamp": timestamp})
            if log:
                return jsonify(log)
            else:
                return {"message": "Log not found"}, 404
        else:
            logs = list(logbook_collection.find())
            return jsonify(logs)

    def post(self):
        try:
            new_log = request.get_json()
            validate(instance=new_log, schema=logbook_schema)
            logbook_collection.insert_one(new_log)
            return {"message": "Log inserted"}, 201
        except ValidationError as e:
            return {"message": str(e)}, 400
        
    def put(self, timestamp):
        updated_data = request.get_json()
        logbook_collection.update_one({"timestamp": timestamp}, {"$set": updated_data})
        return {"message": "Log updated"}, 200
    
    # Inside the LogbookResource class
    def delete(self, timestamp):
        log = logbook_collection.find_one({"timestamp": timestamp})
        if log:
            logbook_collection.delete_one({"timestamp": timestamp})
            return {"message": "Log deleted"}, 200
        else:
            return {"message": "Log not found"}, 404



# API Routes
api.add_resource(LogbookResource, "/logbook", "/logbook/<string:timestamp>")


if __name__ == "__main__":
    app.run(debug=True)
