"""
db_manager.py

"""
import sqlite3

DB_FILENAME = "sapms.db"


def get_connection():
    """
    Opens and returns a connection to the SQLite database.
    Creates the database file automatically if it doesn't exist yet.
    """
    connection = sqlite3.connect(DB_FILENAME)
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialize_database():
    """
    Creates the three required tables if they don't already exist.
    Safe to call every time the app starts — it won't overwrite
    existing data because of 'IF NOT EXISTS'.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            grade_level TEXT NOT NULL,
            enrollment_date TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            score REAL NOT NULL,
            term TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );
    """)

    connection.commit()
    connection.close()
    print(f"Database '{DB_FILENAME}' initialized with students, attendance, and grades tables.")


if __name__ == "__main__":
    initialize_database()