import face_recognition

# ---------------------------------------------------------------------------
# Hardcoded User Database
# ---------------------------------------------------------------------------
# Each user has an ID, a name, and a photo path.
# The "encoding" field will be computed from the image.
user_db = {
    "001": {
        "name": "Lovish",
        # Use absolute path or ensure the relative path is correct relative to the working directory.
        "photo_path": r"image.png",
        "encoding": None
    },
    "002": {
        "name": "Prakhar",
        "photo_path": r"Aut_img.jpg",
        "encoding": None
    },
     "003": {
        "name": "Aditya",
        "photo_path": r"WhatsApp Image 2025-02-12 at 21.09.33_e2b926ae.jpg",
        "encoding": None
    },
     "004": {
        "name": "Lavanya",
        "photo_path": r"C:\Users\Prakhar\Desktop\Face Detection project\WhatsApp Image 2025-02-12 at 21.30.14_e331b2a7.jpg",
        "encoding": None
    }
     ,
     "005": {
        "name": "Nischal",
        "photo_path": r"WhatsApp Image 2025-02-12 at 21.40.20_82c12a4d.jpg",
        "encoding": None
    }
}

# ---------------------------------------------------------------------------
# Module 1: Fetch Users (Simulated Database)
# ---------------------------------------------------------------------------
def fetch_users():
    """
    Simulate fetching all user details.
    For each user, load the image from the hardcoded path,
    compute the face encoding, and update the dictionary.
    
    Returns:
        user_db (dict): The updated user dictionary with face encodings.
    """
    for user_id, user in user_db.items():
        try:
            image = face_recognition.load_image_file(user["photo_path"])
            encodings = face_recognition.face_encodings(image)
           
            if encodings:
                user_db[user_id]["encoding"] = encodings[0]
                print(f"User {user['name']} (ID: {user_id}) enrolled successfully.")
            else:
                print(f"Error: No face detected in {user['photo_path']} for user {user['name']}.")
        except Exception as e:
            print(f"Error processing {user['photo_path']} for user {user['name']}: {e}")
    return user_db

def update_user_encoding(user_id, new_face_encoding):
    """
    Update the face encoding for a given user in the simulated database.
    
    Args:
        user_id (str): The ID of the user to update.
        new_face_encoding (numpy.ndarray): The new face encoding.
    """
    if user_id in user_db:
        user_db[user_id]["encoding"] = new_face_encoding
        print(f"Updated encoding for user {user_id} successfully.")
    else:
        print("User not found.")
