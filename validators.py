import re
from datetime import date, datetime

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_date_of_birth(dob_str: str) -> tuple[bool, str]:
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        if dob >= date.today():
            return False, "Date of birth cannot be today or a future date."
        age = (date.today() - dob).days // 365
        if age > 120:
            return False, "Please enter a valid date of birth."
        return True, ""
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

def validate_blood_value(value, field_name: str, min_val: float, max_val: float) -> tuple[bool, str]:
    try:
        val = float(value)
        if val < min_val or val > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}."
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} must be a numeric value."

def validate_patient_form(full_name, dob_str, email, glucose, haemoglobin, cholesterol) -> list[str]:
    errors = []

    if not full_name or len(full_name.strip()) < 2:
        errors.append("Full name must be at least 2 characters.")

    dob_valid, dob_msg = validate_date_of_birth(str(dob_str))
    if not dob_valid:
        errors.append(dob_msg)

    if not validate_email(email):
        errors.append("Enter a valid email address.")

    ok, msg = validate_blood_value(glucose, "Glucose", 0.1, 600)
    if not ok:
        errors.append(msg)

    ok, msg = validate_blood_value(haemoglobin, "Haemoglobin", 0.1, 25)
    if not ok:
        errors.append(msg)

    ok, msg = validate_blood_value(cholesterol, "Cholesterol", 0.1, 700)
    if not ok:
        errors.append(msg)

    return errors
