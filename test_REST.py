import unittest
from flask_testing import TestCase
from flask_REST import app, db  # replace 'your_flask_app_file' with the actual name of your Flask app file

class TestAPI(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['MONGODB_SETTINGS'] = {
            'db': 'test_db'  # replace with your test database name
        }
        return app

    def setUp(self):
        db.modules.drop()

    def tearDown(self):
        db.modules.drop()

    def test_fetch_all_modules_empty(self):
        response = self.client.get("/modules")
        self.assert200(response)
        self.assertEqual(response.json, [])

    def test_insert_module(self):
        new_module = {
            "inventory": "INV001",
            "position": "A1"
            # ... (other properties)
        }
        response = self.client.post("/modules", json=new_module)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Module inserted"})

    def test_fetch_specific_module_not_found(self):
        response = self.client.get("/modules/INV999")
        self.assertEqual(response.status_code, 404)

    def test_delete_module_not_found(self):
        response = self.client.delete("/modules/INV999")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Module deleted"})


if __name__ == '__main__':
    unittest.main()
