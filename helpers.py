from cs50 import SQL
import requests

from flask import redirect, session
from functools import wraps
import string
import secrets


db = SQL("sqlite:///college.db")


def is_admin(teacher_id):
    result = db.execute("SELECT admin FROM Teachers WHERE id = ?", teacher_id)
    return result[0]['admin'] == 1  # Returns True if admin is True


def generate_username(name, roll_number):
    # Remove spaces and convert name to lowercase
    base = name.replace(" ", "").lower() + roll_number
    suffix = 1
    while True:
        username = f"{base}_{suffix}"
        # Check if username already exists
        result = db.execute("SELECT id FROM Students WHERE username = ?", username)
        if not result:
            break
        suffix += 1
    return username

def generate_password(length=8):
    # Create a secure random password
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password



def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    Decorate routes to require admin login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin(session.get("user")["id"]):
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def get_last_id(table):
    result = db.execute(f"SELECT id FROM {table} ORDER BY id DESC LIMIT 1")
    return result[0]['id'] if result else None



