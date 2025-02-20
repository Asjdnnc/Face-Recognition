import requests
import base64
import numpy as np
import cv2
import face_recognition

API_FETCH_URL = "http://localhost:3000/api/v1/fetch-data"

def fetch_users():
    """
    Fetch users and return a dictionary with face encodings.
    """
    print("Fetching user data...")  # Debug print
    
    response = requests.get(API_FETCH_URL)
    if response.status_code != 200:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return {}

    users = response.json()
    print(f"Received {len(users)} users from API.")  # Debug print

    user_encodings = {}
    for user in users:
        try:
            user_id = user["eid"]
            name = user["name"]
            encoded_image = user["encodedImage"]  # Base64 string

            print(f"Processing user: {name}")  # Debug print

            # Step 1: Decode Base64 image
            image_data = base64.b64decode(encoded_image)
            np_arr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if image is None:
                print(f"Error decoding image for {name}. Skipping.")
                continue

            print(f"Image successfully decoded for {name}")  # Debug print

            # Step 2: Convert to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Step 3: Get face encodings
            encodings = face_recognition.face_encodings(image_rgb)

            if encodings:
                user_encodings[user_id] = {"name": name, "encoding": encodings[0].tolist()}
                print(f"Face encoding extracted for {name}")  # Debug print
            else:
                print(f"No face found for {name}. Skipping.")

        except Exception as e:
            print(f"Error processing {name}: {e}")

    return user_encodings

if __name__ == "__main__":
    users = fetch_users()
    print(f"Final user dictionary: {users}")  # Debug print
