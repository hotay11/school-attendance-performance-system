from validators import (
    validate_non_empty_text,
    validate_age,
    validate_date,
    validate_score,
    validate_attendance_status,
    prompt_until_valid,
)

# TODO: replace with real imports once teammates' modules are ready, e.g.:
# from students import add_student, view_students
# from attendance import record_attendance, view_attendance
# from performance import record_score, view_performance


MENU_TEXT = """
==============================================
 School Attendance and Performance Management
==============================================
1. Add Student
2. View Students
3. Record Attendance
4. View Attendance
5. Record Performance Score
6. View Performance
0. Exit
==============================================
"""


def add_student_flow():
    name = prompt_until_valid("Student name: ", validate_non_empty_text, "Name")
    age = prompt_until_valid("Student age: ", validate_age)
    enrollment_date = prompt_until_valid("Enrollment date (YYYY-MM-DD): ", validate_date)

    # TODO: add_student(name, age, enrollment_date)
    print(f"[Placeholder] Would add student: {name}, age {age}, enrolled {enrollment_date}")


def view_students_flow():
    # TODO: view_students()
    print("[Placeholder] Would display all students here.")


def record_attendance_flow():
    student_id = prompt_until_valid("Student ID: ", validate_non_empty_text, "Student ID")
    date = prompt_until_valid("Date (YYYY-MM-DD): ", validate_date)
    status = prompt_until_valid(
        "Attendance status (present/absent/late/excused): ", validate_attendance_status
    )

    # TODO: record_attendance(student_id, date, status)
    print(f"[Placeholder] Would record attendance: {student_id}, {date}, {status}")


def view_attendance_flow():
    # TODO: view_attendance()
    print("[Placeholder] Would display attendance records here.")


def record_performance_flow():
    student_id = prompt_until_valid("Student ID: ", validate_non_empty_text, "Student ID")
    score = prompt_until_valid("Score (0-100): ", validate_score)

    # TODO: record_score(student_id, score)
    print(f"[Placeholder] Would record score: {student_id}, {score}")


def view_performance_flow():
    # TODO: view_performance()
    print("[Placeholder] Would display performance records here.")


def main():
    while True:
        print(MENU_TEXT)
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student_flow()
        elif choice == "2":
            view_students_flow()
        elif choice == "3":
            record_attendance_flow()
        elif choice == "4":
            view_attendance_flow()
        elif choice == "5":
            record_performance_flow()
        elif choice == "6":
            view_performance_flow()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please pick an option from the menu.")


if __name__ == "__main__":
    main()
