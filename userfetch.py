import requests
import base64
import numpy as np
import cv2
import face_recognition
import time

# API to fetch user data 
API_FETCH_URL = "http://localhost:3000/api/v1/fetch-data"

def fetch_users():
    """
    Fetch users and return a dictionary with face encodings (used in facedetect.py).
    """
    start_time = time.time()
    print("Loading user data, please wait...")

    try:
        response = requests.get(API_FETCH_URL)
    except Exception as e:
        print(f"Failed to fetch data from API: {e}")
        return {}

    if response.status_code != 200:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return {}

    try:
        users = response.json()
    except Exception as e:
        print(f"Error parsing API response: {e}")
        return {}

    user_encodings = {}
    for user in users:
        try:
            user_id = user["eid"]
            name = user["name"]
            encoded_image = user["encodedImage"]  # Base64 string

            # Decode Base64 image
            image_data = base64.b64decode(encoded_image)
            np_arr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if image is None:
                print(f"Error decoding image for {name}. Skipping.")
                continue

            # Convert to RGB and extract face encoding
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(image_rgb)
            if encodings:
                user_encodings[user_id] = {"name": name, "encoding": encodings[0].tolist()}
            else:
                print(f"No face found for {name}. Skipping.")
                # skips the user if no encoding found
        except Exception as e:
            print(f"Error processing {name}: {e}")

    elapsed_time = time.time() - start_time
    print(f"Loaded {len(user_encodings)} users in {elapsed_time:.2f} seconds.")
    return user_encodings

if __name__ == "__main__":
    users = fetch_users()
    print(f"Final user dictionary: {users}")
