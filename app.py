from flask import Flask, render_template, request, Response,redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps
import subprocess
import time
import threading
import os
import sys
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.String(25), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False) 
    time_in = db.Column(db.DateTime, nullable=True,default=None)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    uid = db.Column(db.String(25), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    time_in = db.Column(db.DateTime, nullable=True,default=None)

class BehavioralAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    sleep_detected = db.Column(db.Boolean, default=False)
    phone_usage_detected = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)



users = {
    'teacher': {'username': 'teacher', 'password': 'teacher'},
    'admin': {'username': 'admin', 'password': 'admin'}
}

app.secret_key = secrets.token_hex(32)

@app.route('/')
def home():
    return redirect(url_for('login'))  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == users['teacher']['username'] and password == users['teacher']['password']:
            session['user'] = username  # Store user in session
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        
        elif username == users['admin']['username'] and password == users['admin']['password']:
            session['user'] = username
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', category="danger", message="Invalid login credentials")

    return render_template('login.html')



@app.route('/view_report/<int:student_id>')
def view_report(student_id):
    behaviors = BehavioralAnalysis.query.filter_by(student_id=student_id).all()

    if not behaviors:
        return "No behavioral data found", 404

    sleep_record = next((b for b in behaviors if b.sleep_detected), None)
    phone_record = next((b for b in behaviors if b.phone_usage_detected), None)

    sleep_detected = "Yes" if sleep_record else "No"
    phone_usage_detected = "Yes" if phone_record else "No"

    sleep_time = sleep_record.timestamp.strftime("%Y-%m-%d %H:%M:%S") if sleep_record else "N/A"
    phone_time = phone_record.timestamp.strftime("%Y-%m-%d %H:%M:%S") if phone_record else "N/A"

    report = (
        f"Sleep Detected: {sleep_detected}   Time: {sleep_time}\n"
        f"Phone Usage Detected: {phone_usage_detected}   Time: {phone_time}\n"
    )

    return Response(report, mimetype="text/plain")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    return decorated_function


@app.route('/teacher_dashboard')
@login_required
def teacher_dashboard():
    students = Student.query.all()
    return render_template('teacher.html', students=students)

@app.route('/api/teacher_dashboard')
def api_teacher_dashboard():
    students = Student.query.all()
    
    student_list = [{ "id": user.id, "name": user.name, "uid": user.uid, "gender": user.gender, "attendance": "Present" if user.time_in else "Absent"} for user in students]
    
    return jsonify({"students": student_list})

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    teachers = Teacher.query.all()
    return render_template('admin.html',teachers=teachers)

@app.route('/api/admin_dashboard')
def api_admin_dashboard():
    teachers = Teacher.query.all()
    teacher_list = [{"id": user.id, "name": user.name, "uid": user.uid, "gender": user.gender, "attendance": "Present" if user.time_in else "Absent"} for user in teachers]
        
    return jsonify({"teachers": teacher_list})

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))


@app.route('/register_nfc', methods=['POST'])
def register_nfc():
    try:
        data = request.get_json()
        id=data.get("id","").strip()
        name = data.get("name", "").strip()
        uid = data.get("uid", "").strip().upper()
        gender = data.get("gender", "").strip().capitalize()
        role = data.get("role", "").strip().lower() 

        if not all([name, uid, gender, role]):
            return jsonify({"message": "Missing required fields"}), 400

        if role not in ["student", "teacher"]:
            return jsonify({"message": "Invalid role. Use 'student' or 'teacher'"}), 400

        
        if Student.query.filter_by(uid=uid).first() or Teacher.query.filter_by(uid=uid).first():
            return jsonify({"message": "UID is already registered"}), 400

        
        if role == "student":
            new_user = Student(id=id,name=name, uid=uid, gender=gender)
        else:
            new_user = Teacher(id=id,name=name, uid=uid, gender=gender)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": f"{role.capitalize()} {name} registered successfully"}), 201

    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500


def delayed_facial_recognition():
    time.sleep(30)  #30s to start the facial recognition

    venv_python = os.path.join(os.getcwd(), "env2", "Scripts", "python.exe")

    if not os.path.exists(venv_python): 
        print("Error: Virtual environment not found at", venv_python)
        return

    subprocess.Popen([venv_python, "facial_recognition.py"], stdout=sys.stdout, stderr=sys.stderr)


@app.route('/scan_nfc', methods=['POST'])
def scan_nfc():
    try:
        data = request.get_json()
        uid = data.get("uid", "").strip().upper()

        if not uid:
            return jsonify({"message": "No UID received"}), 400

        student = Student.query.filter_by(uid=uid).first()
        teacher = Teacher.query.filter_by(uid=uid).first()

        if student:
            if student.time_in:
                return jsonify({"message": f"Student {student.name} attendance already recorded."}), 400
            
            student.time_in = datetime.now()
            db.session.commit()
            return jsonify({"message": f"Student {student.name} attendance recorded."}), 200

        elif teacher:
            if teacher.time_in:
                return jsonify({"message": f"Teacher {teacher.name} attendance already recorded."}), 400
            
            teacher.time_in = datetime.now()
            db.session.commit()

            #calling the facial recognition code
            threading.Thread(target=delayed_facial_recognition).start()

            return jsonify({"message": f"Teacher {teacher.name} attendance recorded. Facial recognition will start in 30 seconds."}), 200

        return jsonify({"message": "User not found. Please register the NFC card."}), 404

    except Exception as e:
        return jsonify({"message": "Server Error", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='192.168.1.103', port=5000, debug=True)
