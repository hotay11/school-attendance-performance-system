"""
db_manager.py

"""

import sqlite3

DB_FILENAME = "sapms.db"


class DatabaseManager:
    def __init__(self, db_filename=DB_FILENAME):
        self.connection = sqlite3.connect(db_filename)
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        cursor = self.connection.cursor()

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

        self.connection.commit()

    # ------------------------------------------------------------------
    # Generic query helpers used by every manager file
    # ------------------------------------------------------------------
    def execute(self, query, params=()):
        """For INSERT / UPDATE / DELETE. Returns the cursor (so callers
        can read cursor.lastrowid after an INSERT)."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_all(self, query, params=()):
        """For SELECT statements returning multiple rows."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        """For SELECT statements returning a single row (or None)."""
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def close(self):
        self.connection.close()


if __name__ == "__main__":
    db = DatabaseManager()
    print(f"Database '{DB_FILENAME}' initialized with students, attendance, and grades tables.")
    db.close()