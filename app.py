from flask import Flask, request, jsonify, session, render_template, flash, redirect
import sqlite3
from helpers import is_admin, login_required, generate_username, generate_password, get_last_id, admin_required, generate_daily_attendance
from datetime import timedelta, datetime

app = Flask(__name__)
app.secret_key = "bbede993"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=18)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect("college.db")
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    user = session.get("user")
    try:
        generate_daily_attendance()
    except Exception as e:
        return f"Error generating attendance: {e}", 500

    if user["role"].casefold() == "teacher":
        return render_template("teachers_index.html", user=user)
    elif user["role"].casefold() == "student":
        student_id = user["id"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) as total_classes FROM Attendance WHERE student_id = ?", (student_id,))
        total_classes = cur.fetchone()["total_classes"]

        cur.execute("SELECT COUNT(*) as attended_classes FROM Attendance WHERE student_id = ? AND status = 'Present'", (student_id,))
        attended_classes = cur.fetchone()["attended_classes"]

        attendance_percentage = (attended_classes / total_classes) * 100 if total_classes > 0 else 0

        conn.close()

        return render_template("students_index.html", attendance_percentage=attendance_percentage, user = user)

@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    if not username or not password:
        flash("Username and password are required")
        return redirect("/login")

    try:
        conn = get_db_connection()
        if role == "student":
            result = conn.execute("SELECT id, name FROM Students WHERE username = ? AND password = ?", 
                                  (username, password)).fetchone()
        else:
            result = conn.execute("SELECT id, name FROM Teachers WHERE username = ? AND password = ?", 
                                  (username, password)).fetchone()
        conn.close()

        if not result:
            flash("Please enter a valid username and password")
            return redirect("/login")

        session["user"] = {
            "id": result["id"],
            "name": result["name"],
            "username": username,
            "role": role,
            "admin": is_admin(result["id"]) if role == "teacher" else False
        }
    except Exception as e:
        print(e)
        flash("An error occurred during login")
        return redirect("/login")
    
    return redirect("/")

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route('/add-student', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    if request.method == "POST":
        name = request.form.get("name")
        roll_no = request.form.get("roll_no")

        conn = get_db_connection()
        result = conn.execute("SELECT id FROM Students WHERE roll_number = ?", (roll_no,)).fetchone()

        if result:
            conn.close()
            flash("Roll number already exists", "error")
            return redirect("/add-student")

        username = generate_username(name, roll_no)
        password = generate_password()

        try:
            conn.execute("INSERT INTO Students (name, roll_number, username, password) VALUES (?, ?, ?, ?)", 
                         (name, roll_no, username, password))
            conn.commit()
            conn.close()
            flash(f"Student {name} added successfully. Username: {username}, Password: {password}", "success")
        except Exception as e:
            print(e)
            flash("An error occurred while adding student", "error")

        return redirect("/")

    return render_template("add_students.html")

@app.route('/add-teacher', methods=['GET', 'POST'])
@login_required
@admin_required
def add_teacher():
    if request.method == "POST":
        name = request.form.get("name")
        admin = request.form.get("admin")
        subject = request.form.get("subject")
        id = get_last_id("Teachers") + 1
        username = f"{name}_{id}"
        password = generate_password()
        admin = 1 if admin else 0

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO Teachers (name, username, password, admin) VALUES (?, ?, ?, ?)", 
                         (name, username, password, admin))
            conn.execute("INSERT INTO Subjects (teacher_id, name) VALUES (?, ?)", (id, subject))
            conn.commit()
            conn.close()
            flash(f"Teacher {name} added successfully", "success")
        except Exception as e:
            print(e)
            flash("An error occurred while adding teacher", "error")

        return redirect("/")

    return render_template("add_teacher.html")

@app.route('/students-database')
@login_required
def students_database():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM Students").fetchall()
    conn.close()
    return render_template("students_database.html", students=students)

@app.route('/teachers-database')
@login_required
@admin_required
def teachers_database():
    conn = get_db_connection()
    teachers = conn.execute("SELECT * FROM Teachers").fetchall()
    conn.close()
    return render_template("teachers_database.html", teachers=teachers)

@app.route('/mark-attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    if request.method == "GET":
        today = datetime.now().date()
        teacher_id = session.get("user")["id"]

        conn = get_db_connection()
        subject = conn.execute("SELECT id FROM Subjects WHERE teacher_id = ?", (teacher_id,)).fetchone()

        if not subject:
            conn.close()
            flash("No subject found for the teacher", "warning")
            return redirect("/")
        
        subject_id = subject["id"]
        students = conn.execute("SELECT * FROM Students").fetchall()
        attendance_records = conn.execute("SELECT * FROM Attendance WHERE subject_id = ? AND date = ?", 
                                          (subject_id, today)).fetchall()
        conn.close()

        attendance = {record["student_id"]: record for record in attendance_records}

        if not attendance:
            flash("Attendance not marked today", "warning")
            return redirect("/")

        return render_template("mark_attendance.html", students=students, attendance=attendance, today=today)
    
    try:
        today = datetime.now().date()
        teacher_id = session.get("user")["id"]

        conn = get_db_connection()
        subject = conn.execute("SELECT id FROM Subjects WHERE teacher_id = ?", (teacher_id,)).fetchone()

        if not subject:
            conn.close()
            flash("No subject found for the teacher", "warning")
            return redirect("/")
        
        subject_id = subject["id"]
        students = conn.execute("SELECT * FROM Students").fetchall()

        for student in students:
            status = request.form.get(f"attendance_{student['id']}")  
            status = "Absent" if not status else "Present"

            conn.execute("UPDATE Attendance SET status = ? WHERE student_id = ? AND date = ? AND subject_id = ?", 
                         (status, student['id'], today, subject_id))

        conn.commit()
        conn.close()

    except Exception as e:
        print(e)
        flash("An error occurred while marking attendance", "error")
        return redirect("/")
    
    flash("Attendance marked successfully", "success")
    return redirect("/")
