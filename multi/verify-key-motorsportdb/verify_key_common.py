import json
import os

# DRIVERS KEY
VALID_KEYS_DRIVERS = {
    "firstName",
    "lastName",
    "nickname",
    "dateOfBirth",
    "dateOfDeath",
    "country",
    "seasons"
}
REQUIRED_KEYS_DRIVERS = {
    "firstName",
    "lastName"
}
# TEAMS KEY
VALID_KEYS_TEAMS = {
    "name",
    "country",
    "creationDate",
    "endDate",
    "previous",
    "next",
    "seasons"
}
REQUIRED_KEYS_TEAMS = {
    "name"
}
# RACES KEY
VALID_KEYS_RACES = {
    "name",
    "country",
    "events"
}
REQUIRED_KEYS_RACES = {
    "name"
}

def validate_json_file(file_path, REQUIRED_KEYS, VALID_KEYS):
    errors = []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            return [f"[JSON_ERROR] {file_path}: {e}"]

    keys = set(data.keys())

    # VERIFY NEEDED KEY
    missing_required = REQUIRED_KEYS - keys
    if missing_required:
        for k in missing_required:
            errors.append(f"[MISSING] {file_path}: Needed key '{k}' forget")

    # CHECK UNKNOWN KEY
    unknown_keys = keys - VALID_KEYS
    if unknown_keys:
        for k in unknown_keys:
            errors.append(f"[UNKNOWN] {file_path}: Uknown key '{k}' detected")

    return errors

def validate_drivers(drivers_json_path):
    return validate_json_file(drivers_json_path, REQUIRED_KEYS_DRIVERS, VALID_KEYS_DRIVERS)

def validate_teams(teams_json_path):
    return validate_json_file(teams_json_path, REQUIRED_KEYS_TEAMS, VALID_KEYS_TEAMS)

def validate_races(races_json_path):
    return validate_json_file(races_json_path, REQUIRED_KEYS_RACES, VALID_KEYS_RACES)