import torch
import cv2
import os
import io
import contextlib
import pandas as pd
from datetime import datetime
from deepface import DeepFace
import time
from app import db, Student, BehavioralAnalysis, app

#loading yolov5
model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=True)

#loading haar cascade for sleep detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# webcam default
cap = cv2.VideoCapture(0)

eye_closed_counter = {}
sleep_detection_threshold = 3  


processed_students = set()
marked_absent = set()  


previous_time_in = {}

session_duration=0.5*60

start_time=time.time()


with app.app_context():
    registered_students = {student.name: student for student in Student.query.all()}

while True:

    elapsed_time = time.time() - start_time
    if elapsed_time >= session_duration:
        print("Classroom session over. Stopping the camera...")
        break 

    ret, frame = cap.read()
    if not ret:
        print("Camera frame not received. Exiting...")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(rgb_frame)
    detections = results.pandas().xyxy[0]

    phone_detections = detections[detections["name"] == "cell phone"]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5) 

    detected_students = set()  

    try:
        with contextlib.redirect_stdout(io.StringIO()):
            res = DeepFace.find(frame, db_path="database", enforce_detection=False, model_name="VGG-Face", distance_metric="cosine")
    except Exception as e:
        print(f"DeepFace Error: {e}")
        res = []

    if isinstance(res, list) and len(res) > 0:
        for df in res:
            if isinstance(df, pd.DataFrame) and not df.empty and "identity" in df.columns:
                for identity_path in df["identity"].dropna().tolist():
                    name = os.path.normpath(identity_path).split(os.sep)[-2]
                    if name in registered_students:
                        with app.app_context():
                            student = db.session.query(Student).filter_by(name=name).first()
                            if student:
                                detected_students.add(name)
                                if name in previous_time_in:
                                    print(f"Restoring time_in for {name}.")
                                    student.time_in = previous_time_in.pop(name)
                                    db.session.commit()
                                if student.time_in and name not in processed_students:
                                    print(f"{name} is present.")
                                    processed_students.add(name)

                                existing_record = BehavioralAnalysis.query.filter_by(student_id=student.id).first()
                                if name not in eye_closed_counter:
                                    eye_closed_counter[name] = 0

                                person_eyes = [eye for eye in eyes if (eye[0] >= 0 and eye[1] >= 0)]
                                if not person_eyes:
                                    eye_closed_counter[name] += 1
                                else:
                                    eye_closed_counter[name] = 0

                                if eye_closed_counter[name] >= sleep_detection_threshold:
                                    if not existing_record:
                                        print(f"Creating new record for {name} with sleep detected.")
                                        existing_record = BehavioralAnalysis(student_id=student.id, sleep_detected=True, timestamp=datetime.now())
                                        db.session.add(existing_record)
                                    else:
                                        if not existing_record.sleep_detected:
                                            print(f"Updating sleep detection for {name}.")
                                            existing_record.sleep_detected = True
                                            existing_record.timestamp = datetime.now()
                                    db.session.commit()

                                for _, phone in phone_detections.iterrows():
                                    if not existing_record:
                                        print(f"Creating new record for {name} with phone usage detected.")
                                        existing_record = BehavioralAnalysis(student_id=student.id, phone_usage_detected=True, timestamp=datetime.now())
                                        db.session.add(existing_record)
                                    else:
                                        if not existing_record.phone_usage_detected:
                                            print(f"Updating phone usage for {name}.")
                                            existing_record.phone_usage_detected = True
                                            existing_record.timestamp = datetime.now()
                                    db.session.commit()
    
    with app.app_context():
        for student in registered_students.values():
            if student.name not in detected_students and student.time_in and student.name not in marked_absent:
                print(f"Marking {student.name} as absent.")
                student = db.session.query(Student).filter_by(id=student.id).first()
                previous_time_in[student.name] = student.time_in
                student.time_in = None
                db.session.commit()
                marked_absent.add(student.name)

    cv2.imshow("Face Recognition, Sleep & Phone Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()