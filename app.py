from flask import Flask, request, jsonify,session, render_template, flash, redirect
from cs50 import SQL
from helpers import is_admin, login_required, generate_username, generate_password, get_last_id, admin_required
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "bbede993"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=18)

if __name__ == "__main__":
    app.run(debug=True)

db = SQL("sqlite:///college.db")


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    user = session.get("user")
    print(user)
    return render_template("index.html", user=user)
    

@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    print("\n\n"+role)

    if not username or not password:
        flash("Username and password are required")
        return redirect("/login")

    try:
        if role == "student":
            result = db.execute("SELECT id, name FROM Students WHERE username = ? AND password = ?", username, password)
            if not result:
                flash("Please enter a valid username and password")
                return redirect("/login")
            id = result[0]['id']
            name = result[0]['name']
        else:
            result = db.execute("SELECT id, name FROM Teachers WHERE username = ? AND password = ?", username, password)
            if not result:
                flash("Please enter a valid username and password")
                return redirect("/login")
            id = result[0]['id']
            name = result[0]['name']
        
        session["user"] = {
            "id": id,
            "name": name,
            "username": username,
            "role": role,
            "admin": is_admin(id) if role == "teacher" else False
        }
    except Exception as e:
        print("\n\n", e)
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

        # Check if roll number already exists
        result = db.execute("SELECT id FROM Students WHERE roll_number = ?", roll_no)
        if result:
            flash("Roll number already exists", "error")
            return redirect("/add-student")

        username = generate_username(name, roll_no)
        password = generate_password()

        try:
            db.execute("INSERT INTO Students (name, roll_number, username, password) VALUES (?, ?, ?, ?)", name, roll_no, username, password)
            flash(f"Student {name} added successfully. Username: {username}, Password: {password}", "success")
        except Exception as e:
            print(e)
            flash("An error occurred while adding student", "error")
            return redirect("/add-student")

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

        if not admin:
            admin = 0
        else:
            admin = 1

        try:
            db.execute("INSERT INTO Teachers (name, username, password, admin) VALUES (?, ?, ?, ?)", name, username, password, admin)
            db.execute("INSERT INTO Subjects (teacher_id, name) VALUES (?, ?)", id, subject)
            flash(f"Teacher {name} added successfully", "success")
        except Exception as e:
            print(e)
            flash("An error occurred while adding teacher", "error")
            return redirect("/add-teacher")

        return redirect("/")

    return render_template("add_teacher.html")

@app.route('/students-database')
@login_required
@admin_required
def students_database():
    students = db.execute("SELECT * FROM Students")
    return render_template("students_database.html", students=students)

@app.route('/teachers-database')
@login_required
@admin_required
def teachers_database():
    teachers = db.execute("SELECT * FROM Teachers")
    return render_template("teachers_database.html", teachers=teachers)


@app.route('/mark-attendance', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    if request.method == "GET":
        teacher_id = session.get("user")["id"]
        students = db.execute("SELECT * FROM Students " )
        return render_template("mark_attendance.html", students=students)
    return redirect("/")
        
        

