import requests

# The URL where your Flask API is running
api_url = "http://localhost:5005/modules"  # Replace with your actual API URL

# The new modules data
new_modules = [
    {"moduleID": "PS_40_05-IBA_00001", "position": "cleanroom", "status": "ok",},  # Bari01 data
    {"moduleID": "PS_26_05-IBA_00004", "position": "cleanroom", "status": "ok", "LpGBTFuseId": 3142643356, },  # Bari04 data
    {"moduleID": "PS_40_05_IPG_00001", "position": "cleanroom", "status": "ok", }  # Perugia data
]

# Loop through each module and make a POST request to insert it
for module in new_modules:
    response = requests.post(api_url, json=module)
    if response.status_code == 201:
        print(f"Module {module['moduleID']} inserted successfully.")
    else:
        print(f"Failed to insert module {module['moduleID']}. Status code: {response.status_code}, Response: {response.json()}")

# Note: Replace '...' in the module data with actual values as per your module schema.
