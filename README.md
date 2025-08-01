# face-rec-attendance

![alt text](image.png)

## Project Title

**AI-Powered Facial Recognition Attendance System**

## Aims and Objectives

- Design and implement a system that automates classroom or office attendance using facial recognition.
- Provide a seamless, contactless, and secure way to record staff or student attendance.
- Integrate RFID and facial recognition for enhanced verification and fraud prevention.
- Offer real-time analytics and reporting for administrators.

## Why the Topic

- Manual attendance systems are time-consuming, error-prone, and susceptible to proxy attendance.
- The need for automation and accuracy in attendance management is increasing in both educational and corporate environments.
- Leveraging AI and computer vision can significantly improve efficiency and security.

## Problem Solved

- Eliminates manual attendance marking and reduces administrative workload.
- Prevents buddy-punching and proxy attendance through biometric verification.
- Provides instant reporting and analytics for attendance trends.
- Integrates with existing infrastructure (RFID, databases) for a comprehensive solution.

## Features

- **Facial Recognition:** Uses a webcam to detect and recognize faces ([facerecognition.py](facerecognition.py)).
- **RFID Integration:** Supports RFID card scanning for dual-factor attendance ([server.js](server.js)).
- **Web Dashboard:** Real-time attendance dashboard and analytics ([templates/dashboard.html](templates/dashboard.html)).
- **Admin Panel:** User management, staff registration, and attendance logs ([templates/admin_home.html](templates/admin_home.html)).
- **Password Reset:** Secure password reset via email ([auth.py](auth.py), [utils.py](utils.py)).
- **Role-Based Access:** Restricts access to features based on user roles ([decorators.py](decorators.py), [models.py](models.py)).
- **Live Video Feed:** Streams camera feed to the browser ([facerecognition.py](facerecognition.py), [routes.py](routes.py)).
- **Export Reports:** Download attendance data as PDF or Excel ([templates/dashboard.html](templates/dashboard.html)).

## Technology Stack

- **Backend:** Python, Flask, Flask-Login, Flask-Mail, Flask-PyMongo
- **Frontend:** HTML, Tailwind CSS, JavaScript, Chart.js
- **Database:** MongoDB (via Flask-PyMongo)
- **RFID Middleware:** Node.js, Express, SerialPort, Socket.IO ([server.js](server.js))
- **Face Recognition:** dlib, face_recognition, OpenCV

## How to Run

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   npm install
   ```

2. **Configure environment variables:**  
   Set up your `.env` file for MongoDB URI, mail credentials, and secret keys.

3. **Start the Flask app:**
   ```sh
   python app.py
   ```

4. **Start the RFID middleware (if using RFID):**
   ```sh
   node server.js
   ```

5. **Access the app:**  
   Open [http://127.0.0.1:8001/](http://127.0.0.1:8001/) in your browser.

## Folder Structure

- `app.py` – Main Flask application
- `facerecognition.py` – Face recognition and video streaming logic
- `auth.py`, `models.py`, `routes.py`, `utils.py` – Core backend modules
- `static/` – Static JS and image assets
- `templates/` – HTML templates for all pages
- `server.js` – Node.js middleware for RFID
- `Dockerfile`, `compose.yaml` – Containerization and deployment

## Authors

- [Your Name or Team]

## License

- [Specify your license here]
