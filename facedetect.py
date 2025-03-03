import cv2
import dlib
import face_recognition
import numpy as np
import time
import logging
import subprocess
 # Play a system sound

#import winsound  # For beep sound on Windows

from userfetch import fetch_users   # Fetch user details and encodings.
from update import update_attendance  # Update attendance function.

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
video_source = 0  # Current video source; can be replaced with a URI if needed.
face_predictor = r"shape_predictor_68_face_landmarks.dat" #shape_predictor_68_face_landmarks.dat file must be in folder 

# Configuration parameters.
EAR_THRESHOLD = 0.23          # Threshold below which eyes are considered closed.
REQUIRED_MATCHES = 2          # Consecutive matching frames required to lock onto a candidate.
CHECK_INTERVAL = 2            # Time window (seconds) to monitor for blink events.
BLINKS_REQUIRED = 1           # Number of blink events required for liveness confirmation.
BLINK_RANGE_THRESHOLD = 0.15  # (Not used in this approach.)
SPOOF_THRESHOLD = 4           # Number of consecutive spoof detections before sleeping.
SLEEP_DURATION = 2            # Sleep duration in  seconds.

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
    Capture a live face from the webcam, perform recognition and a liveness check (blink detection),
    and mark attendance only if a valid blink event is detected.
    
    Additional features:
      - Beep sound is played when a live face is confirmed.
      - If spoofing is detected for more than SPOOF_THRESHOLD consecutive times,
        the system goes to sleep for SLEEP_DURATION seconds before restarting.
    """
    cap = cv2.VideoCapture(video_source)
    print("Starting attendance capture. Press 'q' to exit.")

    # Enlarge the display window (does not change processing resolution).
    cv2.namedWindow("Attendance System", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Attendance System", 1280, 720)

    # Initialize dlib's face detector and shape predictor.
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_predictor)

    candidate = None              # Currently matched user id.
    candidate_data = None         # Holds candidate tracking info.
    attended_users = set()        # User IDs already marked as attended.
    consecutive_spoof_count = 0   # Counter for consecutive spoof detections.

    frame_skip = 2                # Process every nth frame.
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue

        frame_proc = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_frame = cv2.cvtColor(frame_proc, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame_proc, cv2.COLOR_BGR2GRAY)

        # Compute live face encoding (assumes one face per frame).
        live_encodings = face_recognition.face_encodings(rgb_frame)
        if live_encodings:
            live_encoding = live_encodings[0]
            best_match_id = None
            best_match_data = None
            min_distance = float("inf")
            for user_id, data in user_db.items():
                if user_id in attended_users:
                    continue
                stored_encoding = data.get("encoding")
                if stored_encoding is None:
                    continue
                distance = np.linalg.norm(np.array(stored_encoding) - np.array(live_encoding))
                if distance < min_distance:
                    min_distance = distance
                    best_match_id = user_id
                    best_match_data = data

            if best_match_id is not None and min_distance < tolerance:
                logging.info(f"Current match: {best_match_data['name']} with distance {min_distance:.4f}")

                # Lock candidate tracking.
                if candidate == best_match_id:
                    candidate_data["match_count"] += 1
                else:
                    candidate = best_match_id
                    candidate_data = {
                        "match_count": 1,
                        "blink_count": 0,          # Count of detected blink events.
                        "eyes_closed": False,      # Current eye state.
                        "start_time": time.time()  # Start time for monitoring.
                    }
                cv2.putText(frame, f"Pending: {best_match_data['name']} ({candidate_data['match_count']}/{REQUIRED_MATCHES})", 
                            (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 2)

                if candidate_data["match_count"] >= REQUIRED_MATCHES:
                    # Use face_recognition to get face location.
                    face_locations = face_recognition.face_locations(rgb_frame)
                    if face_locations:
                        top, right, bottom, left = face_locations[0]
                        rect = dlib.rectangle(left, top, right, bottom)
                        landmarks = predictor(gray, rect)
                        left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                        right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
                        ear = (get_eye_aspect_ratio(left_eye) + get_eye_aspect_ratio(right_eye)) / 2.0
                        cv2.putText(frame, f"EAR: {ear:.2f}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

                        # Blink event detection:
                        if ear < EAR_THRESHOLD:
                            candidate_data["eyes_closed"] = True
                        else:
                            if candidate_data["eyes_closed"]:
                                candidate_data["blink_count"] += 1
                                logging.info(f"Blink detected for {best_match_data['name']}: total blinks {candidate_data['blink_count']}")
                                candidate_data["eyes_closed"] = False

                    # After CHECK_INTERVAL seconds, decide on liveness.
                    if time.time() - candidate_data["start_time"] > CHECK_INTERVAL:
                        if candidate_data["blink_count"] >= BLINKS_REQUIRED:
                            cv2.putText(frame, f"Welcome, {best_match_data['name']}!", (50, 140),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                            logging.info(f"Attendance marked for {best_match_data['name']} (ID: {candidate})")
                            attended_users.add(candidate)
                            update_attendance(candidate, attendance=True)
                            # Play beep sound.
                            #winsound.Beep(1000, 300)
                            #winsound.Beep(1000, 300)
                            play_sound()
                            play_sound()
                            play_sound()
                            play_sound()
                            play_sound()
                            consecutive_spoof_count = 0  # Reset spoof counter on success.
                        else:
                            cv2.putText(frame, "Spoofing Detected", (50, 120),
                                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
                            logging.info("Spoofing detected: Fake Face")
                            consecutive_spoof_count += 1
                            if consecutive_spoof_count >= SPOOF_THRESHOLD:
                                logging.info("Too many spoof detections, sleeping for 2 seconds...")
                                time.sleep(SLEEP_DURATION)
                                consecutive_spoof_count = 0
                        candidate = None
                        candidate_data = None
            else:
                candidate = None
                candidate_data = None
                cv2.putText(frame, "Face not recognized", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
        else:
            candidate = None
            candidate_data = None
            cv2.putText(frame, "No face detected", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def play_sound():
    subprocess.Popen(["afplay", "/System/Library/Sounds/Ping.aiff"])


if __name__ == '__main__':
    users = fetch_users()
    check_attendance(users)
