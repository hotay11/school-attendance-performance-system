from datetime import datetime


def validate_non_empty_text(value, field_name="Input"):
    if value is None or str(value).strip() == "":
        return False, f"{field_name} cannot be empty."
    return True, ""


def validate_age(age, min_age=3, max_age=100):
    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be a whole number."

    if age_int < min_age or age_int > max_age:
        return False, f"Age must be between {min_age} and {max_age}."

    return True, ""


def validate_date(date_str, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(str(date_str).strip(), date_format)
    except (ValueError, TypeError):
        return False, f"Date must be in {date_format} format (e.g. 2026-07-23)."

    return True, ""


def validate_score(score, min_score=0, max_score=100):
    try:
        score_val = float(score)
    except (ValueError, TypeError):
        return False, "Score must be a number."

    if score_val < min_score or score_val > max_score:
        return False, f"Score must be between {min_score} and {max_score}."

    return True, ""


def validate_attendance_status(status, allowed_statuses=None):
    if allowed_statuses is None:
        allowed_statuses = ["present", "absent", "late", "excused"]

    if status is None or str(status).strip().lower() not in allowed_statuses:
        allowed_display = ", ".join(allowed_statuses)
        return False, f"Attendance status must be one of: {allowed_display}."

    return True, ""


def prompt_until_valid(prompt_text, validator_func, *validator_args, **validator_kwargs):
    while True:
        value = input(prompt_text).strip()
        is_valid, message = validator_func(value, *validator_args, **validator_kwargs)
        if is_valid:
            return value
        print(f"Invalid input: {message}")
