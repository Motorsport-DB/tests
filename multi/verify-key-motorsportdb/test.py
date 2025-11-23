import os
from verify_key_common import validate_files_batch
import json

def scan_json_folder():
    config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)

    linux_url_local_files = config_data.get("LINUX_URL_LOCAL_FILES")
    if not linux_url_local_files:
        raise ValueError("LINUX_URL_LOCAL_FILES key is missing in the configuration file.")
    
    BASE_URL = config_data.get("LINUX_URL_LOCAL_FILES")
    drivers_folder = os.path.expanduser(BASE_URL + "/drivers")
    teams_folder = os.path.expanduser(BASE_URL + "/teams")
    races_folder = os.path.expanduser(BASE_URL + "/races")
    
    # Prepare all files for batch processing
    all_files = []
    
    drivers_files = [
        os.path.join(drivers_folder, f) for f in os.listdir(drivers_folder)
        if f.endswith(".json")
    ]
    for file_path in drivers_files:
        all_files.append((file_path, 'driver'))
    
    teams_files = [
        os.path.join(teams_folder, f) for f in os.listdir(teams_folder)
        if f.endswith(".json")
    ]
    for file_path in teams_files:
        all_files.append((file_path, 'team'))
    
    races_files = [
        os.path.join(championship_path, f)
        for championship in os.listdir(races_folder)
        if os.path.isdir(championship_path := os.path.join(races_folder, championship))
        for f in os.listdir(championship_path)
        if f.endswith(".json")
    ]
    for file_path in races_files:
        all_files.append((file_path, 'race'))
    
    print(f"Validating {len(all_files)} JSON files in parallel...")
    print(f"  - {len(drivers_files)} drivers")
    print(f"  - {len(teams_files)} teams")
    print(f"  - {len(races_files)} races")
    
    # Validate all files in parallel
    all_errors = validate_files_batch(all_files)

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
