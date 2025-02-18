import face_recognition
def validate_and_encode_face(image_path):
    """
    Loads an image from the provided path, checks that a face is present,
    and returns the face encoding.
    Raises:
        ValueError: If no face is detected in the provided image.
    """
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise ValueError("No face detected in the provided image.")
    return encodings[0]
