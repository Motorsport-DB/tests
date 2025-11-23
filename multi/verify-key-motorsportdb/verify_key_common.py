import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def validate_files_batch(files_data):
    """Validate multiple JSON files in parallel.
    
    Args:
        files_data: List of tuples (file_path, file_type) where file_type is 'driver', 'team', or 'race'
    
    Returns:
        List of all errors found
    """
    all_errors = []
    total = len(files_data)
    processed = 0
    
    def process_file(file_tuple):
        nonlocal processed
        file_path, file_type = file_tuple
        
        if file_type == 'driver':
            errors = validate_drivers(file_path)
        elif file_type == 'team':
            errors = validate_teams(file_path)
        elif file_type == 'race':
            errors = validate_races(file_path)
        else:
            errors = [f"Unknown file type: {file_type}"]
        
        processed += 1
        if processed % 100 == 0:
            print(f"Progress: {processed}/{total} files validated")
        
        return errors
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_file, file_data) for file_data in files_data]
        
        for future in as_completed(futures):
            try:
                errors = future.result()
                all_errors.extend(errors)
            except Exception as e:
                all_errors.append(f"Error processing file: {e}")
    
    return all_errors