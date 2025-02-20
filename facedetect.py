import cv2
import dlib
import face_recognition
import numpy as np
import time

from userfetch import fetch_users  # Import the fetch_users function from userfetch.py
from update import update_attendance  # Import the attendance update function

def get_eye_aspect_ratio(eye):
    """
    Compute the Eye Aspect Ratio (EAR) given six eye landmark coordinates.
    """
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

def check_attendance(user_db, tolerance=0.5):
    """
    Capture a live face from the webcam, compare it against stored encodings,
    perform liveness detection (blink detection), and mark attendance for
    matching users. Once a user's attendance is marked, they will not be rechecked.
    """
    cap = cv2.VideoCapture(0)
    print("Starting attendance capture. Press 'q' to exit.")
    
    # Initialize dlib's face detector and shape predictor for liveness detection.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r"c:\Users\Prakhar\Desktop\codes\python\opencv\otask1c\shape_predictor_68_face_landmarks.dat")
    
    # Parameters for blink detection.
    blink_count = 0
    start_time = time.time()
    EAR_THRESHOLD = 0.23    # Adjusted threshold for blink detection
    BLINKS_REQUIRED = 2     # Required number of blinks within the check interval
    CHECK_INTERVAL = 2      # Interval (in seconds) to evaluate blink count
    match_counts = {}       # Dictionary to store match count for each user
    REQUIRED_MATCHES = 2    # Number of consecutive matches needed for confirmation
    
    # Dictionary to track which users have already been marked attended.
    attended_users = {}

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        if not ret:
            break

        # Convert frame to RGB and grayscale.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Compute live face encoding using face_recognition (assumes one face per frame).
        live_encodings = face_recognition.face_encodings(rgb_frame)
        if live_encodings:
            live_encoding = live_encodings[0]
            matched_user = None
            matched_user_id = None
            min_distance = float("inf")
            
            # Compare the live encoding against each stored user's encoding.
            for user_id, data in user_db.items():
                # Skip users already marked as attended.
                if user_id in attended_users:
                    continue
                stored_encoding = data.get("encoding")
                if stored_encoding is None:
                    continue
                distance = np.linalg.norm(np.array(stored_encoding) - np.array(live_encoding))
                if distance < min_distance:
                    min_distance = distance
                    matched_user = data
                    matched_user_id = user_id

            if min_distance < 0.5 and matched_user is not None:
                # Increase confirmation count for the matched user.
                if matched_user_id not in match_counts:
                    match_counts[matched_user_id] = 1
                else:
                    match_counts[matched_user_id] += 1
                
                if match_counts[matched_user_id] >= REQUIRED_MATCHES:
                    print(f"Matched user: {matched_user['name']} with distance: {min_distance}")
                    # Perform liveness check using blink detection.
                    faces = detector(gray)
                    if faces:
                        for face in faces:
                            landmarks = predictor(gray, face)
                            left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                            right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
                            left_ear = get_eye_aspect_ratio(left_eye)
                            right_ear = get_eye_aspect_ratio(right_eye)
                            avg_ear = (left_ear + right_ear) / 2.0

                            if avg_ear < EAR_THRESHOLD:  # A blink is detected.
                                blink_count += 1
                                time.sleep(0.1)  # Brief pause to avoid counting a single blink multiple times.
                        
                        # Check if the number of blinks in the CHECK_INTERVAL is sufficient.
                        elapsed_time = time.time() - start_time
                        if elapsed_time > CHECK_INTERVAL:
                            if blink_count >= BLINKS_REQUIRED:
                                cv2.putText(frame, f"Welcome, {matched_user['name']}!", (50, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                print(f"Attendance marked for {matched_user['name']} (ID: {matched_user_id})")
                                # Mark the user as attended so they won't be rechecked.
                                attended_users[matched_user_id] = True
                                # Send attendance data to updatedata.py.
                                update_attendance(matched_user_id, attendance=True)
                            else:
                                cv2.putText(frame, "Spoofing Detected", (50, 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                                print("Spoofing detected: Fake Face")
                            # Reset blink count and timer.
                            blink_count = 0
                            start_time = time.time()
                    else:
                        cv2.putText(frame, "No face for liveness check", (50, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    print(f"Pending confirmation: {matched_user['name']} ({match_counts[matched_user_id]}/{REQUIRED_MATCHES})")
            else:
                match_counts.clear()
                cv2.putText(frame, "Face not recognized", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Attendance System", frame)
                continue
        else:
            cv2.putText(frame, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Fetch user details (simulate database retrieval and enrollment).
    users = fetch_users()
    
    # Print user details and encoding status.
    for uid, details in users.items():
        status = "Encoding exists" if details["encoding"] is not None else "No encoding"
        print(f"User ID: {uid}, Name: {details['name']}, {status}")
    
    # Start the attendance checking process with integrated liveness check.
    check_attendance(users)
