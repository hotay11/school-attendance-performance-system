"""
grade_manager.py
-----------------
Handles recording grades and calculating average scores.

Real schema (see db_manager.py by Manzi):
    grade_id   INTEGER PRIMARY KEY AUTOINCREMENT
    student_id INTEGER NOT NULL
    subject    TEXT NOT NULL
    score      REAL NOT NULL
    term       TEXT NOT NULL
"""

from models import GradeRecord
from validators import validate_non_empty_text, validate_score, prompt_until_valid


class GradeManager:
    """Handles recording grades and computing grade statistics."""

    def __init__(self, db, student_manager):
        self.db = db
        self.student_manager = student_manager

    def record_grades(self):
        print("\n--- Record Grades ---")
        self.student_manager.view_students()

        student_id_raw = prompt_until_valid(
            "Enter Student ID: ", validate_non_empty_text, "Student ID"
        )
        if not student_id_raw.isdigit():
            print("Student ID must be a number.\n")
            return
        student_id = int(student_id_raw)

        if not self.student_manager.student_exists(student_id):
            print("No student found with that ID. Please register them first.\n")
            return

        subject = prompt_until_valid("Enter Subject: ", validate_non_empty_text, "Subject")
        term = prompt_until_valid("Enter Term (e.g. Term 1): ", validate_non_empty_text, "Term")
        score = float(prompt_until_valid("Enter Score (0-100): ", validate_score))

        self.db.execute(
            "INSERT INTO grades (student_id, subject, score, term) VALUES (?, ?, ?, ?)",
            (student_id, subject, score, term),
        )
        print(f"Grade recorded: Student {student_id} - {subject} - {score} ({term})\n")

    def get_grades_for_student(self, student_id):
        rows = self.db.fetch_all(
            "SELECT * FROM grades WHERE student_id = ? ORDER BY term, subject",
            (student_id,),
        )
        return [GradeRecord.from_row(row) for row in rows]

    def calculate_average_grade(self, student_id):
        grades = self.get_grades_for_student(student_id)
        if not grades:
            return None
        return round(sum(g.score for g in grades) / len(grades), 2)

    def performance_report(self):
        print("\n--- Performance Report ---")
        self.student_manager.view_students()

        student_id_raw = prompt_until_valid(
            "Enter Student ID: ", validate_non_empty_text, "Student ID"
        )
        if not student_id_raw.isdigit():
            print("Student ID must be a number.\n")
            return
        student_id = int(student_id_raw)

        student = self.student_manager.get_student(student_id)
        if student is None:
            print("No student found with that ID.\n")
            return

        grades = self.get_grades_for_student(student_id)
        average = self.calculate_average_grade(student_id)

        print(f"\nPerformance Report for {student.full_name} (ID {student_id})")
        print("-" * 45)
        if not grades:
            print("No grade records found for this student.")
        else:
            for grade in grades:
                print(grade)
        print("-" * 45)
        print(f"Average Grade: {average if average is not None else 'N/A'}\n")
