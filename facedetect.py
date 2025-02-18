import cv2
import dlib
import face_recognition
import numpy as np
import time
from userfetch import fetch_users  # Import the fetch_users function from userfetch.py

def get_eye_aspect_ratio(eye):
    """
    Compute the Eye Aspect Ratio (EAR) given six eye landmark coordinates.
    """
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

def check_attendance(user_db):
    """
    Use the webcam to capture a live face, compare it against the stored encodings,
    and then perform liveness detection using blink detection.
    If a match is found and sufficient blinks are detected, mark the corresponding
    user as present.
    """
    cap = cv2.VideoCapture(1)
    print("Starting attendance capture. Press 'q' to exit.")
    
    # Initialize dlib's face detector and shape predictor for liveness detection.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(r"c:\Users\Prakhar\Desktop\codes\python\opencv\otask1c\shape_predictor_68_face_landmarks.dat")
    
    # Parameters for blink detection.
    blink_count = 0
    start_time = time.time()
    EAR_THRESHOLD = 0.23       # Adjusted threshold for blink detection.
    BLINKS_REQUIRED = 2        # Required number of blinks within the check interval.
    CHECK_INTERVAL = 5         # Interval (in seconds) to evaluate blink count.
    
    # Threshold for face recognition (lower is more strict)
    RECOGNITION_THRESHOLD = 0.4

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame to a consistent resolution.
        frame = cv2.resize(frame, (640, 480))

        # Convert frame to RGB (for face_recognition) and grayscale (for landmark detection).
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        # Detect face locations and compute face encodings.
        face_locations = face_recognition.face_locations(rgb_frame)
        live_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if live_encodings:
            live_encoding = live_encodings[0]
            matched_user = None
            matched_user_id = None
            best_distance = float("inf")

            # Compare the live encoding against each stored user's encoding using face distance.
            for user_id, data in user_db.items():
                stored_encoding = data.get("encoding")
                if stored_encoding is None:
                    continue
                distance = face_recognition.face_distance([stored_encoding], live_encoding)[0]
                if distance < best_distance and distance < RECOGNITION_THRESHOLD:
                    best_distance = distance
                    matched_user = data
                    matched_user_id = user_id

            if matched_user is not None:
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

                        if avg_ear < EAR_THRESHOLD:  # Blink detected.
                            blink_count += 1
                            # Brief pause to avoid multiple counts for a single blink.
                            time.sleep(0.1)

                    # Evaluate blink count after the CHECK_INTERVAL.
                    elapsed_time = time.time() - start_time
                    if elapsed_time > CHECK_INTERVAL:
                        if blink_count >= BLINKS_REQUIRED:
                            cv2.putText(frame, f"Welcome, {matched_user['name']}!", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            print(f"Attendance marked for {matched_user['name']} (ID: {matched_user_id})")
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
                cv2.putText(frame, "Face not recognized", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
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
