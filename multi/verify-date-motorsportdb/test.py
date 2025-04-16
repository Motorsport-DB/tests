import os
from verify_date_common import check_date_fields

def scan_dates_in_folder():
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
    
    
    for file_path in drivers_files + teams_files + races_files:
        errors = check_date_fields(file_path)
        all_errors.extend(errors)


    return all_errors


if __name__ == "__main__":
    result = scan_dates_in_folder()

    if result:
        print("❌ verify-date-motorsportdb")
        for err in result:
            print("-", err)
    else:
        print("✅ verify-date-motorsportdb passed successfully!")
