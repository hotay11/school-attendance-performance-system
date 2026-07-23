from validators import (
    validate_non_empty_text,
    validate_age,
    validate_date,
    validate_score,
    validate_attendance_status,
    prompt_until_valid,
)
from db_manager import DatabaseManager
from student_manager import StudentManager
from attendance_manager import AttendanceManager
from grade_manager import GradeManager
from report_manager import ReportManager


MENU_TEXT = """
==============================================
 School Attendance and Performance Management
==============================================
1. Register Student
2. View Students
3. Search Student
4. Update Student
5. Record Attendance
6. Record Grade
7. View Reports (Attendance & Grades)
8. View At-Risk Students
9. Exit
==============================================
"""


class SAPMSApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.student_manager = StudentManager(self.db)
        self.attendance_manager = AttendanceManager(self.db, self.student_manager)
        self.grade_manager = GradeManager(self.db, self.student_manager)
        self.report_manager = ReportManager(
            self.db, self.student_manager, self.attendance_manager, self.grade_manager
        )

    def register_student_flow(self):
        name = prompt_until_valid("Student name: ", validate_non_empty_text, "Name")
        student_class = prompt_until_valid("Class: ", validate_non_empty_text, "Class")
        age = prompt_until_valid("Age: ", validate_age)
        guardian_contact = prompt_until_valid(
            "Guardian contact: ", validate_non_empty_text, "Guardian contact"
        )
        self.student_manager.register_student(name, student_class, age, guardian_contact)

    def view_students_flow(self):
        self.student_manager.view_students()

    def search_student_flow(self):
        query = prompt_until_valid(
            "Enter student ID or name to search: ", validate_non_empty_text, "Search query"
        )
        self.student_manager.search_student(query)

    def update_student_flow(self):
        student_id = prompt_until_valid("Student ID to update: ", validate_non_empty_text, "Student ID")
        name = prompt_until_valid("New name: ", validate_non_empty_text, "Name")
        student_class = prompt_until_valid("New class: ", validate_non_empty_text, "Class")
        age = prompt_until_valid("New age: ", validate_age)
        guardian_contact = prompt_until_valid(
            "New guardian contact: ", validate_non_empty_text, "Guardian contact"
        )
        self.student_manager.update_student(student_id, name, student_class, age, guardian_contact)

    def record_attendance_flow(self):
        student_id = prompt_until_valid("Student ID: ", validate_non_empty_text, "Student ID")
        date = prompt_until_valid("Date (YYYY-MM-DD): ", validate_date)
        status = prompt_until_valid(
            "Attendance status (Present/Absent/Late): ",
            validate_attendance_status,
            ["present", "absent", "late"],
        )
        self.attendance_manager.record_attendance(student_id, date, status)

    def record_grade_flow(self):
        student_id = prompt_until_valid("Student ID: ", validate_non_empty_text, "Student ID")
        subject = prompt_until_valid("Subject: ", validate_non_empty_text, "Subject")
        term = prompt_until_valid("Term: ", validate_non_empty_text, "Term")
        score = prompt_until_valid("Score (0-100): ", validate_score)
        self.grade_manager.record_grade(student_id, subject, term, score)

    def view_reports_flow(self):
        self.attendance_manager.generate_attendance_report()
        self.grade_manager.generate_performance_report()

    def view_at_risk_flow(self):
        self.report_manager.view_at_risk_students()

    def run(self):
        while True:
            print(MENU_TEXT)
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.register_student_flow()
            elif choice == "2":
                self.view_students_flow()
            elif choice == "3":
                self.search_student_flow()
            elif choice == "4":
                self.update_student_flow()
            elif choice == "5":
                self.record_attendance_flow()
            elif choice == "6":
                self.record_grade_flow()
            elif choice == "7":
                self.view_reports_flow()
            elif choice == "8":
                self.view_at_risk_flow()
            elif choice == "9":
                self.db.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please pick an option from the menu.")


if __name__ == "__main__":
    app = SAPMSApp()
    app.run()
