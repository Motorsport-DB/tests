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
            # Use a custom JSON decoder to detect duplicate keys
            data = json.load(f, object_pairs_hook=check_duplicate_keys)
        except json.JSONDecodeError as e:
            return [f"[JSON_ERROR] {file_path}: {e}"]
        except ValueError as e:  # Catch duplicate key errors
            return [f"[DUPLICATE_KEY_ERROR] {file_path}: {e}"]

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
            errors.append(f"[UNKNOWN] {file_path}: Unknown key '{k}' detected")

    return errors


def check_duplicate_keys(pairs):
    """Helper function to detect duplicate keys in JSON."""
    seen_keys = set()
    for key, value in pairs:
        if key in seen_keys:
            raise ValueError(f"Duplicate key '{key}' found")
        seen_keys.add(key)
    return dict(pairs)

def validate_drivers(drivers_json_path):
    return validate_json_file(drivers_json_path, REQUIRED_KEYS_DRIVERS, VALID_KEYS_DRIVERS)

def validate_teams(teams_json_path):
    return validate_json_file(teams_json_path, REQUIRED_KEYS_TEAMS, VALID_KEYS_TEAMS)

def validate_races(races_json_path):
    return validate_json_file(races_json_path, REQUIRED_KEYS_RACES, VALID_KEYS_RACES)