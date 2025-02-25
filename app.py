from flask import Flask, render_template, request, jsonify
import cv2
import face_recognition
import numpy as np
import os
import json

app = Flask(__name__)

# Path to store known face encodings
KNOWN_FACES_DIR = "faces"
ATTENDANCE_FILE = "data/attendance.json"

# Load known faces
known_faces = []
known_names = []

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump({}, f)

# Load attendance data
def load_attendance():
    with open(ATTENDANCE_FILE, "r") as f:
        return json.load(f)

def save_attendance(attendance_data):
    with open(ATTENDANCE_FILE, "w") as f:
        json.dump(attendance_data, f, indent=4)

# Encode known faces
for filename in os.listdir(KNOWN_FACES_DIR):
    img = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
    encoding = face_recognition.face_encodings(img)
    
    if encoding:
        known_faces.append(encoding[0])
        known_names.append(os.path.splitext(filename)[0])

# Initialize webcam
def recognize_faces():
    cap = cv2.VideoCapture(0)
    attendance = load_attendance()

    while True:
        _, frame = cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"

            if True in matches:
                match_idx = matches.index(True)
                name = known_names[match_idx]

                # Mark attendance
                if name not in attendance:
                    attendance[name] = "Present"
                    save_attendance(attendance)

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/attendance")
def get_attendance():
    return jsonify(load_attendance())

if __name__ == "__main__":
    app.run(debug=True)
