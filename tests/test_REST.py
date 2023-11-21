import unittest
from flask_testing import TestCase
from app.flask_REST import (
    app,
    db,
) 

class TestAPI(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["MONGODB_SETTINGS"] = {
            "db": "unittest_db"  # replace with your test database name
        }
        return app

    def setUp(self):
        db.modules.drop()
        db.logbook.drop()
        db.current_cabling_map.drop()
        db.tests.drop()
        db.cables.drop()
        db.cables_templates.drop()

    def tearDown(self):
        db.modules.drop()
        db.logbook.drop()
        db.current_cabling_map.drop()
        db.tests.drop()
        db.cables.drop()
        db.cables_templates.drop()

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

    def test_addTest(self):
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

        response = self.client.post("/addTest", json=new_test)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"message": "Entry inserted"})

        # check if the test was inserted in the modules
        response = self.client.get("/modules/M1")
        retrieved_module = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(retrieved_module['tests'], ["T001"])

    def test_insert_cable_templates(self):
        cable_templates = [
            {
                "type": "exapus",
                "internalRouting": {
                    "1": [1, 2],
                    "2": [3, 4],
                    "3": [5, 6],
                    "4": [7, 8],
                    "5": [9, 10],
                    "6": [11, 12]
                }
            },
            {
                "type": "extfib",
                "internalRouting": {
                    "1": 1,
                    "2": 2,
                    "3": 3,
                    "4": 4,
                    "5": 5,
                    "6": 6,
                    "7": 7,
                    "8": 8,
                    "9": 9,
                    "10": 10,
                    "11": 11,
                    "12": 12
                }
            },
            {
                "type": "dodecapus",
                "internalRouting": {
                    "1": 3,
                    "2": 6,
                    "3": 9,
                    "4": 12,
                    "5": 2,
                    "6": 5,
                    "7": 8,
                    "8": 11,
                    "9": 1,
                    "10": 4,
                    "11": 7,
                    "12": 10
                }
            }
        ]

        for template in cable_templates:
            response = self.client.post("/cable_templates", json=template)
            self.assertEqual(response.status_code, 201)
            self.assertIn("message", response.json)
            self.assertEqual(response.json["message"], "Cable template inserted")

            cable_type = template["type"]
            response = self.client.get(f"/cable_templates/{cable_type}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["type"], cable_type)


    def test_cabling_map(self):
        cables_to_add = [
            {'cableID': 'cable1', 'detSide': 'det1', 'crateSide': 'cable2'},
            {'cableID': 'cable2', 'detSide': 'cable1', 'crateSide': 'crate1'},
            {'cableID': 'cable3', 'detSide': 'cable4', 'crateSide': 'crate2'},
            {'cableID': 'cable4', 'detSide': 'det2', 'crateSide': 'cable3'},
        ]

        for cable in cables_to_add:
            response = self.client.post('/cables', json=cable)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.get_json(), {"message": "Entry inserted"})

        response = self.client.get('/cables')

        response = self.client.post('/cablingMap', json={'detSide': ["cable1"], 'crateSide': ["cable3", "cable4"]})
        json_data = response.get_json()
        # left to right detSid to crateSide
        expected_result_cable1 = ["detSide", "cable1", "cable2", "crateSide"]
        expected_result_cable3 = ['crateSide', 'cable3', 'cable4', 'detSide']
        expected_result_cable4 = ['crateSide', 'cable4', 'detSide']
        self.assertEqual(json_data["cable1"], expected_result_cable1)
        self.assertEqual(json_data["cable3"], expected_result_cable3)
        self.assertEqual(json_data["cable4"], expected_result_cable4)


if __name__ == "__main__":
    unittest.main()
