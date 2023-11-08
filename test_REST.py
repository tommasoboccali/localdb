import unittest
from flask_testing import TestCase
from flask_REST import (
    app,
    db,
)  # replace 'your_flask_app_file' with the actual name of your Flask app file


class TestAPI(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["MONGODB_SETTINGS"] = {
            "db": "test_db"  # replace with your test database name
        }
        return app

    def setUp(self):
        db.modules.drop()
        db.logbook.drop()
        db.current_cabling_map.drop()
        db.tests.drop()

    def tearDown(self):
        db.modules.drop()
        db.logbook.drop()
        db.current_cabling_map.drop()
        db.tests.drop()

    def test_fetch_all_modules_empty(self):
        response = self.client.get("/modules")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_insert_module(self):
        new_module = {
            "moduleID": "INV001",
            "position": "cleanroom",
            "status": "readyformount",
            # ... (other properties)
        }
        response = self.client.post("/modules", json=new_module)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Module inserted"})

        response = self.client.get("/modules/INV001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["moduleID"], "INV001")       

    def test_fetch_specific_module_not_found(self):
        response = self.client.get("/modules/INV999")
        self.assertEqual(response.status_code, 404)

    def test_delete_module_not_found(self):
        response = self.client.delete("/modules/INV999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Module deleted"})

    def test_insert_log(self):
        new_log = {"timestamp": "2023-11-03T14:21:29Z", "event": "Module added", "operator": "John Doe"}
        response = self.client.post("/logbook", json=new_log)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Log inserted"})

    def test_fetch_log_not_found(self):
        response = self.client.get("/logbook/2023-11-03T15:00:00Z")
        self.assertEqual(response.status_code, 404)

    def test_delete_log_not_found(self):
        response = self.client.delete("/logbook/2023-11-03T15:00:00Z")
        self.assertEqual(response.status_code, 404)

    def test_delete_log(self):
        # First, let's insert a log entry
        new_log = {"timestamp": "2023-11-03T14:21:29Z", "event": "Module added", "operator": "John Doe"}
        self.client.post("/logbook", json=new_log)

        # Now, let's delete it
        response = self.client.delete("/logbook/2023-11-03T14:21:29Z")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Log deleted"})

    def test_insert_cabling_map(self):
        test_data = {
            "ID": "TestID",
            "detSide": [{"channel": 1}],
            "crateSide": "TestCrate",
            "Type": "TestType"
        }

        response = self.client.post('/current_cabling_map', json=test_data)
        self.assertEqual(response.status_code, 201)

        inserted_data = self.client.get('/current_cabling_map/TestID')
        self.assertIsNotNone(inserted_data)

    def test_invalid_cabling_map(self):
        test_data = {
            "ID": "TestID",
            "detSide": [{"channel": 1}]
        }

        response = self.client.post('/current_cabling_map', json=test_data)
        self.assertEqual(response.status_code, 400)

    def test_get_cabling_map(self):
        test_data = {
            "ID": "TestID",
            "detSide": [{"channel": 1}],
            "crateSide": "TestCrate",
            "Type": "TestType"
        }
        self.client.post('/current_cabling_map', json=test_data)
        response = self.client.get('/current_cabling_map/TestID')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TestID', response.data)

    def test_insert_and_retrieve_test(self):
        new_test = {
            "testID": "T001",
            "modules_list": ["M1", "M2"],
            "testType": "Type1",
            "testDate": "2023-11-01",
            "testStatus": "completed",
            "testResults": {}
        }

        # Insert
        response = self.client.post("/tests", json=new_test)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Entry inserted"})

        # Retrieve
        response = self.client.get("/tests/T001")
        retrieved_test = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(retrieved_test['testID'], "T001")

    def test_delete_test(self):
        # Delete
        new_test = {
            "testID": "T001",
            "modules_list": ["M1", "M2"],
            "testType": "Type1",
            "testDate": "2023-11-01",
            "testStatus": "completed",
            "testResults": {}
        }

        # Insert
        insert = self.client.post("/tests", json=new_test)
        response = self.client.delete("/tests/T001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Entry deleted"})

        # Verify Deletion
        response = self.client.get("/tests/T001")
        self.assertEqual(response.status_code, 404)

        """    def newTest(self):
        try:
            new_entry = request.get_json()
            validate(instance=new_entry, schema=tests_schema)
            tests_collection.insert_one(new_entry)
        
            for moduleID in new_entry["modules_list"]:
                modules_collection.update_one({"moduleID": moduleID}, {"$push": {"tests": new_entry["testID"]}})
            return {"message": "Entry inserted"}, 201
        
        except ValidationError as e:
            return {"message": str(e)}, 400
        """

    def test_newTest(self):
        new_test = {
            "testID": "T001",
            "modules_list": ["M1", "M2"],
            "testType": "Type1",
            "testDate": "2023-11-01",
            "testStatus": "completed",
            "testResults": {}
        }
        # create modules 
        new_module = {
            "moduleID": "M1",
            "position": "cleanroom",
            "status": "readyformount",
            # ... (other properties)
        }
        response = self.client.post("/modules", json=new_module)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Module inserted"})
        new_module = {
            "moduleID": "M2",
            "position": "cleanroom",
            "status": "readyformount",
            # ... (other properties)
        }
        response = self.client.post("/modules", json=new_module)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Module inserted"})

        response = self.client.post("/newTest", json=new_test)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Entry inserted"})

        # check if the test was inserted in the modules
        response = self.client.get("/modules/M1")
        retrieved_module = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(retrieved_module['tests'], ["T001"])

if __name__ == "__main__":
    unittest.main()
