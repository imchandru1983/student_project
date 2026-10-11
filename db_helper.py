# db_helper.py
import sqlite3

DATABASE_NAME = "users.db"

def init_db():
    """Initializes the database and creates necessary tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 1. Existing Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')

    # 2. New Student Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            guardian_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email_address TEXT NOT NULL,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')

    conn.commit()
    conn.close()

# Add a new user
def add_user(username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Verify user credentials
def verify_user(username, password):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def fetch_users():
    """Retrieves all users from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Change a user's password
def change_password(username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("UPDATE users SET password = ? WHERE username = ?", (password, username))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def fetch_applications():
    """Retrieves all student applications from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_applications")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Add a new student application
def add_application(username, name, guardian_name, dob, mobile, email_address):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO student_applications (username, name, guardian_name, dob, mobile, email_address) VALUES (?, ?, ?, ?, ?, ?)", (username, name, guardian_name, dob, mobile, email_address))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

# Add a new user
def add_user(username, password):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def delete_applications(application_ids):
    """Deletes student applications based on a list of application IDs."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.executemany("DELETE FROM student_applications WHERE application_id = ?", [(app_id,) for app_id in application_ids])
    conn.commit()
    conn.close()

def update_application_field(application_id, field_name, new_value):
    """Updates a specific field of a student application."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    query = f"UPDATE student_applications SET {field_name} = ? WHERE application_id = ?"
    cursor.execute(query, (new_value, application_id))
    conn.commit()
    conn.close()