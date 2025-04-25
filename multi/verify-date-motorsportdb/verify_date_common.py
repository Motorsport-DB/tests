import re
import json
from datetime import datetime

def is_valid_date(value):
    # If the value is a list, check each element
    if isinstance(value, list):
        return all(is_valid_date(item) for item in value)

    # YYYY
    if isinstance(value, str):
        if re.fullmatch(r"\d{4}", value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        # YYYY-MM-DD
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            try:
                datetime.strptime(value, "%Y-%m-%d")
                return True
            except ValueError:
                return False

    return False


def check_date_fields(file_path):
    errors = []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return [f"[JSON_ERROR] {file_path}: {e}"]

    for key, value in data.items():
        if "date" in key.lower():
            if not is_valid_date(value):
                errors.append(
                    f"[INVALID_DATE] {file_path}: champ '{key}' a une valeur invalide '{value}'"
                )

    return errors
