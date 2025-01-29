import sqlite3
from flask import redirect, session
from functools import wraps
import string
import secrets

DATABASE = "college.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Returns dict-like rows
    return conn

def is_admin(teacher_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT admin FROM Teachers WHERE id = ?", (teacher_id,))
    result = cur.fetchone()
    conn.close()
    return result["admin"] == 1 if result else False

def generate_username(name, roll_number):
    base = name.replace(" ", "").lower() + roll_number
    suffix = 1
    conn = get_db_connection()
    cur = conn.cursor()
    while True:
        username = f"{base}_{suffix}"
        cur.execute("SELECT id FROM Students WHERE username = ?", (username,))
        if not cur.fetchone():
            break
        suffix += 1
    conn.close()
    return username

def generate_password(length=8):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin(session.get("user")["id"]):
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def get_last_id(table):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    conn.close()
    return result["id"] if result else None

def generate_daily_attendance(today):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM Students")
    students = cur.fetchall()
    
    cur.execute("SELECT id FROM Subjects")
    subjects = cur.fetchall()

    if not students or not subjects:
        conn.close()
        raise ValueError("No students or subjects found in the database.")

    for student in students:
        for subject in subjects:
            cur.execute(
                "SELECT id FROM Attendance WHERE student_id = ? AND subject_id = ? AND date = ?",
                (student["id"], subject["id"], today)
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO Attendance (student_id, subject_id, date, status) VALUES (?, ?, ?, ?)",
                    (student["id"], subject["id"], today, "Absent")
                )
    conn.commit()
    conn.close()