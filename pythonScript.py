import requests

API_URL = "http://localhost:3000/fetch-data"
API_URL2 = "http://localhost:3000/python"
#get request to fetch data from server
response = requests.get(API_URL)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Failed to fetch data")

# Data to send
Python_data = {
    "name": "Aditya Kumar",
    "eid": 101,
    "message": "Hello from Python!"
}

response2 = requests.post(API_URL2, json=Python_data)
print("Response from server:", response2.json())