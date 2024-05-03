'''import cv2
import face_recognition
import numpy as np
#import serial

# Open serial connection to Arduino
#ser = serial.Serial('COM3', 9600)  # Change 'COM3' to match your Arduino's serial port

# Load images for recognition
person1_image = face_recognition.load_image_file('suman.jpg')  # Replace 'person1.jpg' with the image file for person 1
#person2_image = face_recognition.load_image_file('person2.jpg')  # Replace 'person2.jpg' with the image file for person 2
# Add more images for additional persons if needed

# Encode the faces in the images
person1_face_encoding = face_recognition.face_encodings(person1_image)[0]
#person2_face_encoding = face_recognition.face_encodings(person2_image)[0]
# Encode faces for additional persons if needed

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        # Compare the face encoding in the frame with the encodings of all persons
        #matches = face_recognition.compare_faces([person1_face_encoding, person2_face_encoding], face_encoding)
        matches = face_recognition.compare_faces([person1_face_encoding], face_encoding)

        #if True in matches:
            # Face recognized, send command to Arduino
            #ser.write(b'1')  # Send '1' to Arduino
        #else:
            # Face not recognized, send command to Arduino
            #ser.write(b'0')  # Send '0' to Arduino

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()'''
'''
import cv2
import face_recognition

# Load your image
known_image = face_recognition.load_image_file("suman.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare face encoding with the known face encoding
        results = face_recognition.compare_faces([known_encoding], face_encoding)
        name = "Unknown"
        if results[0]:
            name = "Suman"

        # Draw rectangle around the face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw label with name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
'''
import cv2
import face_recognition
import serial
import time

# Load known images and create a dictionary of face encodings
known_encodings = {}
known_encodings["Suman"] = face_recognition.face_encodings(face_recognition.load_image_file("suman.jpg"))[0]
#known_encodings["Person2"] = face_recognition.face_encodings(face_recognition.load_image_file("person2.jpg"))[0]
# Add more persons as needed

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Initialize serial communication with Arduino
ser = serial.Serial('COM5', 9600)  # Change 'COM3' to match your Arduino's serial port
time.sleep(2)  # Wait for Arduino to initialize

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find all face locations and encodings in the current frame
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

        # Send signal to Arduino if a specific person is recognized
        if name == "Person1":
            ser.write(b'1')  # Send '1' to Arduino
        elif name == "Person2":
            ser.write(b'2')  # Send '2' to Arduino

        # Draw rectangle around the face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw label with name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
