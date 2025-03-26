# SmartClass
An AI-powered system that automates attendance tracking and student behavior monitoring in classrooms
SmartClass: AI-Powered Classroom Management System
# 📌 Overview
SmartClass is an AI-driven system designed to automate attendance tracking and monitor student behavior in classrooms. By leveraging facial recognition technology, it streamlines administrative tasks and enhances the overall educational experience.​RFID module is responsible for automated attendance tracking using RFID/NFC cards. Each student and teacher is assigned an NFC card, which is scanned at the classroom entrance using an ESP32-based RFID reader. The scanned data is then processed to mark attendance and initiate facial recognition-based behavioral analysis.

# 🌟 Key Features
- **NFC Card-Based Attendance:** Each student and teacher uses an NFC card for entry.
- **ESP32-Based RFID Reader:** Detects and verifies NFC card IDs at the entrance.
- **Automated Attendance Logging:** Data is sent to the database for real-time tracking.
- **Teacher-Based Session Activation:** Facial recognition starts only after the teacher's scan.
- **Automated Attendance Tracking:** Utilizes facial recognition to record student attendance in real-time.​
- **Behavior Monitoring:** Monitors and analyzes student behavior to identify patterns and provide insights.​
- **Comprehensive Reporting:** Generates detailed reports on attendance and behavior for educators and administrators.​
- **User-Friendly Interface:** Intuitive design ensures ease of use for both staff and students.​


# 🏗️ Tech Stack  
- **Backend:** Python with Flask framework  
- **Frontend:** HTML, CSS  
- **Database:** SQLite  
- **Hardware:** ESP32 microcontroller for IoT integration  
- **AI/ML:** OpenCV for facial recognition
## 📂 Project Structure  

```sh
SmartClass/
├── backend/
│   ├── app.py                  
│   ├── database.py              
│   ├── face_recognition.py      
├── frontend/
│   ├── index.html               
│   ├── styles.css               
├── hardware/
│   ├── esp32_code.ino           
├── models/
│   ├── trained_model.pkl        
├── reports/
│   ├── attendance_reports/      
│   ├── behavior_reports/        
├── static/
│   ├── images/                  
├── templates/
│   ├── dashboard.html           
├── README.md                    
├── requirements.txt              
├── LICENSE                      
```
## ⚡ Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/Mirza-Muhammed/SmartClass.git
```
cd SmartClass


### 2️⃣ Set Up Virtual Environment 

```sh
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

### 3️⃣ Install Dependencies:
```sh
pip install -r requirements.txt
```
### 4️⃣ Run the Application:
```sh
python app.py
```
The application will be accessible at http://127.0.0.1:5000/.

# 📄 Documentation
For detailed documentation and user guides, please refer to the project's GitHub repository.

# 🤝 Contributing
We welcome contributions to enhance SmartClass. Please fork the repository and submit a pull request with your improvements.

# 🛡️ License
This project is licensed under the MIT License. See the LICENSE file for details.
