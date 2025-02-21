# Face Recognition Attendance System

A modern web-based attendance system that uses face recognition to track and manage attendance. The web interface is deployed on Render, and users only need to run the face detection script locally.

## Live Demo
Visit the live application at: https://face-recognition-kshe.onrender.com/

## Features

- 👤 Face Recognition based attendance
- 🔐 Secure Admin Authentication
- 📊 Real-time Attendance Tracking
- 👥 User Management System
- 📸 Live Camera Integration
- 🔍 Search Functionality
- 📱 Responsive Design
- 📊 Attendance History

## Local Setup (Face Detection Only)

You only need to run the face detection script locally to capture and process attendance. The web interface is already deployed and accessible online.

### Prerequisites

- Python 3.8 or higher
- Webcam
- Internet connection

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/face-recognition-attendance.git
cd face-recognition-attendance
```
2. Install Python dependencies:
```bash
pip install opencv-python
pip install face_recognition
pip install requests
pip install dlib
pip install numpy
```
3. Run the face detection script:
```bash
python facedetect.py
```

## Using the System

1. **Web Interface (Online)**
   - Visit https://face-recognition-kshe.onrender.com/
   - Login with admin credentials
   - Add new users with their photos
   - View and manage attendance records
   - Search users by Employee ID

2. **Face Detection (Local)**
   - Run the face detection script on your local machine
   - The script will access your webcam
   - Detected faces will be automatically matched with the database
   - Attendance will be updated in real-time on the web interface

## Admin Access

Contact the system administrator for admin login credentials to access the web interface.

## Troubleshooting

If you encounter issues with the face detection script:

1. Ensure your webcam is properly connected
2. Check your internet connection
3. Verify Python and required packages are correctly installed
4. Make sure the script has permission to access your camera

## Security Note

The face detection script communicates with the deployed server securely. All data transmission is encrypted and protected.
