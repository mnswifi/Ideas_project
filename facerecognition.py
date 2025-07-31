import face_recognition
import cv2
import numpy as np
import os
import concurrent.futures
from datetime import datetime, timedelta

# Load multiple known faces
known_face_encodings = []
known_face_names = []
known_faces_dir = "pictures"

for filename in os.listdir(known_faces_dir):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(known_faces_dir, filename)
        image = face_recognition.load_image_file(image_path)

        encodings = face_recognition.face_encodings(image)
        if encodings:  # Ensure the image contains at least one face
            known_face_encodings.append(encodings[0])
            known_face_names.append(os.path.splitext(filename)[0].replace("_", "/"))  # Use filename as the person's name

# Parallel face comparison function
def compare_faces_parallel(face_encoding):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.35)
    name = "Alien"

    if True in matches:
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        name = known_face_names[best_match_index]

    return name

def water_mark(frame):
    frame = cv2.resize(frame, (1000, 600))  # Resize to standardize frame size
    cv2.putText(frame, 'Idea AI Project', (650, 590), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 61, 72), 2)
    return frame

def display_in_browser(mongo, socketio):
    """Generator function to stream video frames with face recognition."""
    vid = cv2.VideoCapture(0)  # Use webcam (or replace with RTSP URL)
    frame_count = 0
    process_every_n_frames = 2  # Process every Nth frame

    while True:
        ret, frame = vid.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame_count += 1
        face_locations, face_names = [], []

        if frame_count % process_every_n_frames == 0:  # Process every Nth frame
            # Convert frame from BGR to RGB
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Parallel face recognition
            with concurrent.futures.ThreadPoolExecutor() as executor:
                face_names = list(executor.map(compare_faces_parallel, face_encodings))

            for name in face_names:
                if name != "Alien":
                    print(f"Recognized: {name}")

                    # Simulate RFID card data
                    #card_data = mongo.db.card_db.find_one({"staff_id": name})
                    # if not card_data:
                    #     print("Error: Card not registered")
                    #     continue

                    full_name = "Aniekan Inyang"
                    directorate = "DNPT"
                    today_date = datetime.now().strftime('%d/%m/%Y')

                    # Check if an attendance entry already exists for today
                    existing_attendance = mongo.db.attendance.find_one({
                        "staff_id": name,
                        "time_in": {"$regex": f"^{today_date}"}  # Matches today's date
                    })

                    if not existing_attendance:
                        # Record attendance
                        attendance_status = 'Present'
                        attendance_record = {
                            "name": full_name,
                            'staff_id': name,
                            'directorate': directorate,
                            "rfid": "simulated_card_id",
                            "time_in": datetime.now().strftime('%d/%m/%Y %H:%M'),
                            "time_out": None,
                            "status": "Present",
                            "timestamp": datetime.now().strftime('%d/%m/%Y %H:%M')
                        }
                        card_info = {
                            "full_name": full_name,
                            "staff_id": name,
                            "directorate": directorate,
                            "time": datetime.now().strftime('%H:%M'),
                            'status': attendance_status
                        }
                        socketio.emit('update_data', card_info)
                        print('Card info: ',card_info)
                        mongo.db.attendance.insert_one(attendance_record)
                        print(f"📝 Attendance Recorded: {name} - {attendance_record['time_in']}")
                    else:
                        # Person has already clocked in, check if they are trying to clock out
                        # Calculate time difference between time_in and current time
                        time_in = datetime.strptime(existing_attendance["time_in"], '%d/%m/%Y %H:%M')
                        current_time = datetime.now()

                        # Check if 2 minutes have passed since clock-in
                        if current_time - time_in < timedelta(minutes=2):
                            print(f"🚫 {name} cannot sign out yet. Please wait for 2 minutes.")
                        else:
                            # If the person swipes again, update time_out
                            # Uncomment the following lines to enable the functionality for time-out recording
                            mongo.db.attendance.update_one(
                                {"_id": existing_attendance["_id"]},  # Find the existing record
                                {"$set": {"time_out": current_time.strftime('%d/%m/%Y %H:%M')}}  # Update time_out
                            )
                            print(f"🚪 Time OUT recorded for {name} at {current_time.strftime('%H:%M')}")


        # Draw face boxes and labels
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (205, 0, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 100, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 4)

        frame = water_mark(frame)

        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Yield frame for browser streaming
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    vid.release()

# ...existing code...


# def display_in_browser(mongo, socketio):
#     """Generator function to stream video frames with face recognition."""
#     vid = cv2.VideoCapture(0)  # Use webcam (or replace with RTSP URL)
#     # vid = cv2.VideoCapture("rtsp://admin:PwSetit2023!@192.168.1.64:554/streaming/channels/101"http://192.168.137.182:81/stream)
#     #
    
#     frame_count = 0
#     process_every_n_frames = 2  # Process every Nth frame

#     while True:
#         ret, frame = vid.read()
#         if not ret:
#             print("Failed to capture frame")
#             break

#         frame_count += 1
#         face_locations, face_names = [], []

#         if frame_count % process_every_n_frames == 0:  # Process every Nth frame
#             # Convert frame from BGR to RGB
#             small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#             rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

#             # Detect faces
#             face_locations = face_recognition.face_locations(rgb_frame, model="hog")
#             face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#             # Parallel face recognition
#             with concurrent.futures.ThreadPoolExecutor() as executor:
#                 face_names = list(executor.map(compare_faces_parallel, face_encodings))

#             for name in face_names:
#                 if name != "Alien":
#                     print(f"Recognized: {name}")


#                     # Retrieve the latest swiped RFID card
#                     # swipe_data = mongo.db.swipes.find_one(sort=[("_id", -1)])
#                     swipe_data = mongo.db.swipes.find_one({'staff_id': name}, sort=[("_id", -1)])
#                     if not swipe_data:
#                         print("⚠️ No RFID swipe found for this user")
#                         continue
                    
#                     card_id = swipe_data["card_id"]

#                     # Get card owner from card_db
#                     card_data = mongo.db.card_db.find_one({"staff_id": card_id})
#                     if not card_data:
#                         print("Error: Card not registered")
#                         continue
                    
                    

#                     rfid_staff_id = f"{card_data['staff_id']}"
#                     rfid_time = swipe_data['time']
#                     current_time = datetime.now().strftime('%d/%m/%Y %H:%M')

#                     # Compare face name with RFID name
#                     if rfid_staff_id == name and rfid_time[:10] == current_time:
#                         full_name = f'{card_data["first_name"]} {card_data["last_name"]}'
#                         directorate = card_data['directorate']
#                         today_date = datetime.now().strftime('%d/%m/%Y')

#                         # Check if an attendance entry already exists for today
#                         existing_attendance = mongo.db.attendance.find_one({
#                             "staff_id": name,
#                             "time_in": {"$regex": f"^{today_date}"}  # Matches today's date
#                         })

#                         if not existing_attendance:
#                         # Record attendance
#                             attendance_status = 'Present'
#                             attendance_record = {
#                                 "name": full_name,
#                                 'staff_id': name,
#                                 'directorate': directorate,
#                                 "rfid": card_id,
#                                 "time_in": datetime.now().strftime('%d/%m/%Y %H:%M'),
#                                 "time_out": None,
#                                 "status": "Present"
#                             }
#                             card_info = {
#                                 "full_name": f'{card_data["first_name"]} {card_data["last_name"]}',
#                                 "staff_id": card_data["staff_id"],
#                                 "directorate": card_data["directorate"],
#                                 "time": datetime.now().strftime('%H:%M'),
#                                 'status': attendance_status
#                             }
#                             socketio.emit('update_data', card_info)
#                             mongo.db.attendance.insert_one(attendance_record)
#                             print(f"📝 Attendance Recorded: {name} - {attendance_record['time_in']}")
#                         else:
#                             # If the person swipes again, update time_out
#                             mongo.db.attendance.update_one(
#                                 {"_id": existing_attendance["_id"]},  # Find the existing record
#                                 {"$set": {"time_out": datetime.now().strftime('%d/%m/%Y %H:%M')}}  # Update time_out
#                             )
#                             print(f"🚪 Time OUT recorded for {name} at {datetime.now().strftime('%H:%M')}")
#                     else:
#                         print(f"❌ Face ({name}) does not match RFID ({rfid_staff_id})")

#         # Draw face boxes and labels
#         for (top, right, bottom, left), name in zip(face_locations, face_names):
#             top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
#             cv2.rectangle(frame, (left, top), (right, bottom), (205, 0, 0), 2)
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 100, 0), cv2.FILLED)
#             cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 4)

#         frame = water_mark(frame)

#         # Convert frame to JPEG format
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
        
#         # Yield frame for browser streaming
#         yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     vid.release()


if __name__ == "__main__":
    print("Testing face recognition...")
    test_image = face_recognition.load_image_file("test.jpg")  # Replace with an actual image
    test_encoding = face_recognition.face_encodings(test_image)[0]
    print(compare_faces_parallel(test_encoding))


#192.168.137.73