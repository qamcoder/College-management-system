from cs50 import SQL
db = SQL("sqlite:///college.db")

attendance = db.execute("SELECT * FROM Attendance WHERE date = ? and  subject_id = ?", "2025-01-15", 1)

print(attendance)  # Returns a list of dictionaries
current_attendance = {record['student_id']: record for record in attendance}
print(f"\n\n{current_attendance[1]}")  # Returns a dictionary of dictionaries

# The difference in output:
# In Jinja, `attendance.get(student.id)` would retrieve a single record for the given student ID.
# In Python, `current_attendance` is a dictionary where the keys are student IDs and the values are the corresponding records.
# You can now access a specific student's attendance record using `current_attendance[student_id]`.
