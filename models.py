"""
models.py

"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    student_id: Optional[int]
    first_name: str
    last_name: str
    date_of_birth: str
    grade_level: str
    enrollment_date: str
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_row(cls, row):
        # row order matches the students table column order
        return cls(
            student_id=row[0],
            first_name=row[1],
            last_name=row[2],
            date_of_birth=row[3],
            grade_level=row[4],
            enrollment_date=row[5],
        )

    def __str__(self):
        return (f"[{self.student_id}] {self.first_name} {self.last_name} "
                f"- {self.grade_level} (DOB: {self.date_of_birth}, "
                f"Enrolled: {self.enrollment_date})")


@dataclass
class AttendanceRecord:
    attendance_id: Optional[int]
    student_id: int
    date: str
    status: str

    @classmethod
    def from_row(cls, row):
        return cls(
            attendance_id=row[0],
            student_id=row[1],
            date=row[2],
            status=row[3],
        )

    def __str__(self):
        return f"[{self.attendance_id}] Student {self.student_id} - {self.date}: {self.status}"


@dataclass
class GradeRecord:
    grade_id: Optional[int]
    student_id: int
    subject: str
    score: float
    term: str

    @classmethod
    def from_row(cls, row):
        return cls(
            grade_id=row[0],
            student_id=row[1],
            subject=row[2],
            score=row[3],
            term=row[4],
        )

    def __str__(self):
        return f"[{self.grade_id}] Student {self.student_id} - {self.subject} ({self.term}): {self.score}"
