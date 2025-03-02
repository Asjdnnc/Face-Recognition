import requests

# API endpoint for attendance updates.
API_URL2 = "https://face-recognition-kshe.onrender.com/api/v1/update-attendance"

def update_attendance(user_id, attendance=True):
    """
    Update attendance data for the given user by sending a POST request to the API.
    The data is sent in the format:
        {
            "eid": 101,
            "status": "present"
        }
    """
    # Create the payload with the correct status value.
    payload = {
        "eid": user_id,
        "isMatched": True
    }
    
    try:
        response = requests.post(API_URL2, json=payload)
        print (payload)
        if response.status_code == 200:
            print(f"Attendance updated for user {user_id}: attendance = {attendance}")
        else:
            print(f"Failed to update attendance for user {user_id}. Response: {response.text}")
    except Exception as e:
        print(f"Exception occurred while updating attendance for user {user_id}: {e}")
