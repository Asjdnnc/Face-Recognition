import requests

API_URL = "http://localhost:3000/python"

# Data to send
data = {
    "name": "Aditya Kumar",
    "age": 19,
    "message": "Hello from Python!"
}

response = requests.post(API_URL, json=data)
print("Response from server:", response.json())