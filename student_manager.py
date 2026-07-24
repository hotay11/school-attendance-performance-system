"""
student_manager.py

Handles everything related to students: registering a new student,
viewing the full list, searching by ID/name, and updating a
student's details.

Author: Chavyra

Depends on:
    - db_manager.py (Manzi): get_connection() returns the SQLite connection
    - models.py (Manzi): provides the Student class
    - validators.py (Brandon): every function returns a tuple
      (is_valid: bool, message: str)
        - validate_non_empty_text(value, field_name="Input")
        - validate_date(date_str, date_format="%Y-%m-%d")

Real schema of the 'students' table (see db_manager.py):
    student_id      INTEGER PRIMARY KEY AUTOINCREMENT
    first_name      TEXT NOT NULL
    last_name       TEXT NOT NULL
    date_of_birth   TEXT NOT NULL   ('YYYY-MM-DD')
    grade_level     TEXT NOT NULL   (e.g. "Grade 5", "S1")
    enrollment_date TEXT NOT NULL   ('YYYY-MM-DD')
"""

from models import Student
from validators import validate_non_empty_text, validate_date


class StudentManager:
    """
    Handles CRUD operations (Create, Read, Update) for students.
    Never creates its own connection: it is injected by main.py
    (e.g. StudentManager(db_manager.get_connection())).
    """

    def __init__(self, db_connection):
        """
        db_connection: SQLite connection object returned by
        db_manager.get_connection()
        """
        self.conn = db_connection
        self.cursor = self.conn.cursor()

    # ------------------------------------------------------------------
    # 1. Register a new student
    # ------------------------------------------------------------------
    def register_student(self, first_name, last_name, date_of_birth,
                          grade_level, enrollment_date):
        """
        Adds a new student to the 'students' table.
        Returns the created Student object, or None if the data is invalid.
        """
        is_valid, message = validate_non_empty_text(first_name, "First name")
        if not is_valid:
            print(f"Error: {message}")
            return None

        is_valid, message = validate_non_empty_text(last_name, "Last name")
        if not is_valid:
            print(f"Error: {message}")
            return None

        is_valid, message = validate_date(date_of_birth)
        if not is_valid:
            print(f"Error: {message}")
            return None

        is_valid, message = validate_non_empty_text(grade_level, "Grade level")
        if not is_valid:
            print(f"Error: {message}")
            return None

        is_valid, message = validate_date(enrollment_date)
        if not is_valid:
            print(f"Error: {message}")
            return None

        self.cursor.execute(
            """
            INSERT INTO students
                (first_name, last_name, date_of_birth, grade_level, enrollment_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (first_name, last_name, date_of_birth, grade_level, enrollment_date),
        )
        self.conn.commit()

        new_id = self.cursor.lastrowid
        print(f"Student '{first_name} {last_name}' registered successfully (ID {new_id}).")

        return Student(
            student_id=new_id,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            grade_level=grade_level,
            enrollment_date=enrollment_date,
        )

    # ------------------------------------------------------------------
    # 2. View all students
    # ------------------------------------------------------------------
    def view_all_students(self):
        """
        Returns a list of Student objects representing all students.
        """
        self.cursor.execute(
            """
            SELECT student_id, first_name, last_name, date_of_birth,
                   grade_level, enrollment_date
            FROM students
            """
        )
        rows = self.cursor.fetchall()

        students = [self._row_to_student(row) for row in rows]

        if not students:
            print("No students registered yet.")

        return students

    # ------------------------------------------------------------------
    # 3. Search by ID or name (first or last name)
    # ------------------------------------------------------------------
    def search_student(self, keyword):
        """
        Searches for one or more students by exact ID or by name
        (partial match on first_name / last_name).
        Returns a list of Student objects (empty if nothing found).
        """
        keyword = str(keyword).strip()

        if keyword.isdigit():
            self.cursor.execute(
                """
                SELECT student_id, first_name, last_name, date_of_birth,
                       grade_level, enrollment_date
                FROM students
                WHERE student_id = ? OR first_name LIKE ? OR last_name LIKE ?
                """,
                (int(keyword), f"%{keyword}%", f"%{keyword}%"),
            )
        else:
            self.cursor.execute(
                """
                SELECT student_id, first_name, last_name, date_of_birth,
                       grade_level, enrollment_date
                FROM students
                WHERE first_name LIKE ? OR last_name LIKE ?
                """,
                (f"%{keyword}%", f"%{keyword}%"),
            )

        rows = self.cursor.fetchall()
        results = [self._row_to_student(row) for row in rows]

        if not results:
            print(f"No student found for '{keyword}'.")

        return results

    # ------------------------------------------------------------------
    # 4. Check whether a student exists (used by attendance_manager
    #    and grade_manager to validate a student_id before adding
    #    an attendance record or a grade)
    # ------------------------------------------------------------------
    def student_exists(self, student_id):
        """
        Returns True if a student with this ID exists in the database.
        """
        self.cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?", (student_id,)
        )
        return self.cursor.fetchone() is not None

    # ------------------------------------------------------------------
    # 5. Update a student's information
    # ------------------------------------------------------------------
    def update_student(self, student_id, first_name=None, last_name=None,
                        date_of_birth=None, grade_level=None,
                        enrollment_date=None):
        """
        Updates one or more fields of an existing student.
        Only pass the fields you want to change (the others stay None).
        Returns True if the update succeeded, False otherwise.
        """
        if not self.student_exists(student_id):
            print(f"Error: no student with ID {student_id}.")
            return False

        fields = []
        values = []

        if first_name is not None:
            is_valid, message = validate_non_empty_text(first_name, "First name")
            if not is_valid:
                print(f"Error: {message}")
                return False
            fields.append("first_name = ?")
            values.append(first_name)

        if last_name is not None:
            is_valid, message = validate_non_empty_text(last_name, "Last name")
            if not is_valid:
                print(f"Error: {message}")
                return False
            fields.append("last_name = ?")
            values.append(last_name)

        if date_of_birth is not None:
            is_valid, message = validate_date(date_of_birth)
            if not is_valid:
                print(f"Error: {message}")
                return False
            fields.append("date_of_birth = ?")
            values.append(date_of_birth)

        if grade_level is not None:
            is_valid, message = validate_non_empty_text(grade_level, "Grade level")
            if not is_valid:
                print(f"Error: {message}")
                return False
            fields.append("grade_level = ?")
            values.append(grade_level)

        if enrollment_date is not None:
            is_valid, message = validate_date(enrollment_date)
            if not is_valid:
                print(f"Error: {message}")
                return False
            fields.append("enrollment_date = ?")
            values.append(enrollment_date)

        if not fields:
            print("No changes provided.")
            return False

        values.append(student_id)
        query = f"UPDATE students SET {', '.join(fields)} WHERE student_id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()

        print(f"Student ID {student_id} updated successfully.")
        return True

    # ------------------------------------------------------------------
    # Internal helper: converts a SQL row into a Student object
    # ------------------------------------------------------------------
    def _row_to_student(self, row):
        return Student(
            student_id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=row[3],
            grade_level=row[4],
            enrollment_date=row[5],
        )
