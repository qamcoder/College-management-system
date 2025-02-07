# College-management-system
#### Video Demo:  https://youtu.be/LH99Q20VUj8
#### Description:  

The College Management System is a web application designed to efficiently manage student records, teacher information, and student attendance. The system provides role-based access for admin teachers, non-admin teachers, and students, ensuring smooth management and tracking of academic data.

## Key Features

### Admin Teachers:
1. **Add Teachers**: Admin teachers can enter teacher details such as name, subject, and admin status. The system auto-generates their username and password for login, ensuring secure and unique credentials for each teacher.
2. **Add Students**: Admin teachers can enter student details such as name and roll number. The system auto-generates their username and password for login, simplifying the process of student registration.
3. **View Teachers Database**: Admin teachers have access to a structured list of all registered teachers, including their names, usernames, and admin status. This feature helps in managing and reviewing teacher information efficiently.
4. **View Students Database**: Admin teachers can access a structured list of all enrolled students, including their names, roll numbers, and usernames. This feature aids in managing student records and ensuring data accuracy.

### Non-Admin Teachers:
1. **Mark Attendance**: Non-admin teachers can record attendance for all students in their assigned subject on the current date. This feature ensures that attendance is tracked accurately and efficiently.
2. **View Students Database**: Non-admin teachers can access and review student records, helping them stay informed about their students' details and academic progress.

### Students:
1. **View Attendance**: Students can access a user-friendly interface to check their attendance records and percentage. This feature helps students stay informed about their attendance status and encourages them to maintain good attendance.

## System Workflow:
1. **Daily Attendance Verification**: When a user logs in, the system automatically verifies if the daily attendance has been recorded. This ensures that attendance is tracked consistently and accurately.
2. **Automatic Attendance Initialization**: If attendance has not been initialized, the system sets all students as absent by default for every subject on that date. This feature ensures that attendance is recorded even if a teacher forgets to mark it.
3. **Attendance Update by Teachers**: Teachers can later update the attendance status for their respective subjects. This feature allows teachers to correct any errors and ensure that attendance records are accurate.

## Technical Details:
1. **Flask Framework**: The application is built using the Flask framework, which provides a lightweight and flexible foundation for web development.
2. **SQLite Database**: The system uses an SQLite database to store student, teacher, and attendance records. SQLite is a lightweight and efficient database solution that is easy to set up and manage.
3. **Role-Based Access Control**: The system implements role-based access control to ensure that users can only access features and data relevant to their roles. Admin teachers have access to all features, while non-admin teachers and students have limited access based on their roles.
4. **Password Security**: The system uses secure password hashing to ensure that user passwords are stored securely. This feature helps protect user data and prevent unauthorized access.
5. **Responsive Design**: The application features a responsive design that ensures it works well on various devices, including desktops, tablets, and smartphones. This feature enhances the user experience and makes the application accessible to a wider audience.

## Installation and Setup:
1. **Clone the Repository**: Clone the repository to your local machine using the following command:
    ```sh
    git clone https://github.com/yourusername/college-management-system.git
    ```
2. **Install Dependencies**: Navigate to the project directory and install the required dependencies using pip:
    ```sh
    pip install -r requirements.txt
    ```
3. **Initialize the Database**: Run the following command to initialize the database and create the necessary tables:
    ```sh
    python init_db.py
    ```
4. **Run the Application**: Start the Flask application by running the following command:
    ```sh
    flask run
    ```
5. **Access the Application**: Open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

## Usage:
1. **Login**: Users can log in using their username and password. The system will redirect them to the appropriate dashboard based on their role.
2. **Admin Dashboard**: Admin teachers can add new teachers and students, view the teachers' and students' databases, and manage other administrative tasks.
3. **Teacher Dashboard**: Non-admin teachers can mark attendance for their assigned subjects and view the students' database.
4. **Student Dashboard**: Students can view their attendance records and percentage.

## Future Enhancements:
1. **Email Notifications**: Implement email notifications to inform students and teachers about important updates and reminders.
2. **Grade Management**: Add a feature to manage and track student grades, providing a comprehensive academic record.
3. **Parent Access**: Allow parents to access their children's attendance and academic records, enhancing communication between the school and parents.
4. **Mobile Application**: Develop a mobile application to provide a more convenient and accessible way for users to interact with the system.

This system enhances efficiency, reduces manual workload, and ensures accurate tracking of attendance and student records. It provides a comprehensive solution for managing academic data and improving communication between teachers, students, and administrators.
