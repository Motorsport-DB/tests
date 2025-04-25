import os
from verify_key_common import validate_drivers, validate_teams, validate_races

def scan_json_folder():
    all_errors = []
    
    drivers_folder = os.path.expanduser("~/clone-motorsportdb/drivers")
    teams_folder = os.path.expanduser("~/clone-motorsportdb/teams")
    races_folder = os.path.expanduser("~/clone-motorsportdb/races")
    
    drivers_files = [
        os.path.join(drivers_folder, f) for f in os.listdir(drivers_folder)
        if f.endswith(".json")
    ]
    teams_files = [
        os.path.join(teams_folder, f) for f in os.listdir(teams_folder)
        if f.endswith(".json")
    ]
    races_files = [
        os.path.join(championship_path, f)
        for championship in os.listdir(races_folder)
        if os.path.isdir(championship_path := os.path.join(races_folder, championship))
        for f in os.listdir(championship_path)
        if f.endswith(".json")
    ]

    for file_path in drivers_files:
        errors = validate_drivers(file_path)
        all_errors.extend(errors)
    for file_path in teams_files:
        errors = validate_teams(file_path)
        all_errors.extend(errors)
    for file_path in races_files:
        errors = validate_races(file_path)
        all_errors.extend(errors)

    return all_errors

if __name__ == "__main__":
    result = scan_json_folder()

    if result:
        print("❌ verify-key-motorsportdb")
        for r in result:
            print("-", r)
        exit(1)
    else:
        print("✅ verify-key-motorsportdb passed successfully!")
