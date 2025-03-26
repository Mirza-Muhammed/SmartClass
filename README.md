# SmartClass
An AI-powered system that automates attendance tracking and student behavior monitoring in classrooms
SmartClass: AI-Powered Classroom Management System
# 📌 Overview
SmartClass is an AI-driven system designed to automate attendance tracking and monitor student behavior in classrooms. By leveraging facial recognition technology, it streamlines administrative tasks and enhances the overall educational experience.​

# 🌟 Key Features
Automated Attendance Tracking: Utilizes facial recognition to record student attendance in real-time.​
Behavior Monitoring: Monitors and analyzes student behavior to identify patterns and provide insights.​
Comprehensive Reporting: Generates detailed reports on attendance and behavior for educators and administrators.​
User-Friendly Interface: Intuitive design ensures ease of use for both staff and students.​
GitHub
# 🏗️ Tech Stack
Backend: Python with Flask framework​
Frontend: HTML, CSS​
Database: SQLite​
Hardware: ESP32 microcontroller for IoT integration​
AI/ML: OpenCV for facial recognition​
## 📂 Project Structure  

```sh
SmartClass/
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── database.py              # Database connection and operations
│   ├── face_recognition.py      # Face recognition model and functions
├── frontend/
│   ├── index.html               # Frontend user interface
│   ├── styles.css               # CSS for styling the interface
├── hardware/
│   ├── esp32_code.ino           # Code for ESP32 microcontroller integration
├── models/
│   ├── trained_model.pkl        # Pre-trained face recognition model
├── reports/
│   ├── attendance_reports/      # Generated attendance reports
│   ├── behavior_reports/        # Generated behavior reports
├── static/
│   ├── images/                  # Stored images for recognition
├── templates/
│   ├── dashboard.html           # Dashboard page
├── README.md                    # Project documentation
├── requirements.txt              # Dependencies for the project
├── LICENSE                       # License file
## ⚡ Installation & Setup

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/Mirza-Muhammed/SmartClass.git
cd SmartClass
```

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
The application will be accessible at http://127.0.0.1:5000/.
```
# 📄 Documentation
For detailed documentation and user guides, please refer to the project's GitHub repository.

# 🤝 Contributing
We welcome contributions to enhance SmartClass. Please fork the repository and submit a pull request with your improvements.

# 🛡️ License
This project is licensed under the MIT License. See the LICENSE file for details.
