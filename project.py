import cv2
import face_recognition
from pyfirmata import Arduino, SERVO
from time import sleep

# Define Arduino port and pin
port = 'COM5'
pin = 9

# Initialize Arduino board and servo
board = Arduino(port)
board.digital[pin].mode = SERVO

# Load known images and create a dictionary of face encodings
known_encodings = {}
known_encodings["Suman"] = face_recognition.face_encodings(face_recognition.load_image_file("suman.jpg"))[0]

# Initialize video capture
video = cv2.VideoCapture(0)

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        print("Failed to capture video frame")
        break

    # Face recognition
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare face encoding with the known face encodings
        name = "Unknown"
        for known_name, known_encoding in known_encodings.items():
            results = face_recognition.compare_faces([known_encoding], face_encoding)
            if results[0]:
                name = known_name
                break

        # Control the servo based on the recognized face
        if name == "Suman":
            board.digital[pin].write(90)  # Rotate servo to 90 degrees for Person1
        else:
            board.digital[pin].write(0)  # Rotate servo to 0 degrees for all other cases

    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
video.release()
cv2.destroyAllWindows()
