import cv2
import face_recognition
import threading
import time
import pyautogui
import pandas as pd
from send_email import send_email_alert
from get_location import get_current_location
import os

# Load CSV containing detailed person data
data = pd.read_csv("missing_data.csv")

# Load known face encodings and names
known_encodings = []
known_names = []
known_filenames = []

folder_path = "missing_faces"

for filename in os.listdir(folder_path):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(folder_path, filename)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            known_names.append(name)
            known_filenames.append(filename)
            print(f"✅ Loaded and encoded: {name}")
        else:
            print(f"❌ No face found in {filename}")

detection_count = {name: 0 for name in known_names}
last_popup_time = {}

# Function to send alert and popup
def alert_with_email(name, age, gender, last_seen):
    print(f"📩 Sending alert for {name}...")
    location = get_current_location()

    message = (
        f"👤 Name: {name}\n"
        f"🎂 Age: {age}\n"
        f"🚺 Gender: {gender}\n"
        f"📍 Last Seen: {last_seen}\n"
        f"📍 Detected At: {location}"
    )

    send_email_alert(name, location, age, gender, last_seen)

    pyautogui.alert(
        text=message,
        title="Missing Person Detected",
        button="OK"
    )

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("❗ Camera Error")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_index = matches.index(True)
            matched_filename = known_filenames[matched_index]

            try:
                person_info = data[data['filename'] == matched_filename].iloc[0]

                name = person_info['name']
                age = person_info['age']
                gender = person_info['gender']
                last_seen = person_info['last_seen']

                print(f"✅ {name} detected! | Age: {age}, Gender: {gender}, Last Seen: {last_seen}")

                # Show the matched person's image
                image_path = os.path.join("missing_faces", matched_filename)
                if os.path.exists(image_path):
                    detected_img = cv2.imread(image_path)
                    resized_img = cv2.resize(detected_img, (300, 300))
                    cv2.imshow(f"Photo of {name}", resized_img)

                detection_count[name] += 1
                current_time = time.time()

                if name not in last_popup_time or (current_time - last_popup_time[name] > 30):
                    last_popup_time[name] = current_time
                    detection_count[name] = 0
                    threading.Thread(target=alert_with_email, args=(name, age, gender, last_seen)).start()

            except IndexError:
                print(f"❗ No details found in CSV for {matched_filename}")
                name = "Unknown"

        else:
            print("❌ Unknown person detected")

        # Draw box and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition Surveillance", frame)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
