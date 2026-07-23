"""
models.py
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    student_id: Optional[int]  # None until saved to the database (auto-assigned)
    first_name: str
    last_name: str
    date_of_birth: str      # stored as 'YYYY-MM-DD'
    grade_level: str        # e.g. "Grade 5", "S1", etc.
    enrollment_date: str    # stored as 'YYYY-MM-DD'


@dataclass
class AttendanceRecord:
    attendance_id: Optional[int]  # None until saved to the database
    student_id: int               # links back to a Student
    date: str                     # stored as 'YYYY-MM-DD'
    status: str                   # e.g. "Present", "Absent", "Late"


@dataclass
class GradeRecord:
    grade_id: Optional[int]  # None until saved to the database
    student_id: int          # links back to a Student
    subject: str
    score: float
    term: str                # e.g. "Term 1", "Term 2"