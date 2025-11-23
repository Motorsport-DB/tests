from check_errors_commons import check_console_errors_batch
import os
import json

# Load config
config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
with open(config_path, "r") as f:
    config = json.load(f)

URL = config.get("URL_LOCAL_TEST", "http://192.168.1.33:8043")
BASE_PATH = os.path.expanduser(config.get("LINUX_URL_LOCAL_FILES", "~/clone-motorsportdb"))

errors = []

# Get all drivers and teams
drivers_files = [
    f for f in os.listdir(os.path.join(BASE_PATH, "drivers"))
    if f.endswith(".json")
]
teams_files = [
    f for f in os.listdir(os.path.join(BASE_PATH, "teams"))
    if f.endswith(".json")
]
races_files = []
races_path = os.path.join(BASE_PATH, "races")

for championship in os.listdir(races_path):
    championship_path = os.path.join(races_path, championship)
    if os.path.isdir(championship_path):
        for race_file in os.listdir(championship_path):
            if race_file.endswith(".json"):
                race_year = race_file.replace(".json", "")
                races_files.append((championship, race_year))

drivers = [f.split('/')[-1].strip().replace(".json", "") for f in drivers_files]
teams = [f.split('/')[-1].strip().replace(".json", "") for f in teams_files]

total_drivers = len(drivers)
total_teams = len(teams)
total_races = len(races_files)

def verify_errors_console():
    # Prepare all URLs for batch processing
    all_urls = []
    
    # Add driver URLs
    for driver in drivers:
        url = f"{URL}/driver.html?id={driver}"
        all_urls.append((url, "driver", driver))
    
    # Add team URLs
    for team in teams:
        url = f"{URL}/team.html?id={team}"
        all_urls.append((url, "team", team))
    
    # Add race URLs
    for championship, year in races_files:
        url = f"{URL}/race.html?id={championship}&year={year}"
        all_urls.append((url, "race", f"{championship}/{year}"))
    
    print(f"Testing {len(all_urls)} pages in parallel...")
    print(f"  - {total_drivers} drivers")
    print(f"  - {total_teams} teams")
    print(f"  - {total_races} races")
    
    # Process all URLs in parallel
    results = check_console_errors_batch(all_urls)
    
    # Collect errors
    for url, page_type, identifier, errors_console, warnings_console in results:
        for error_console in errors_console:
            errors.append(f"[CHECK-ERRORS-MOTORSPORTDB - BROKEN LINK] - ({identifier}) errors in {url} = {error_console}")
        for warning_console in warnings_console:
            print(f"[⚠️] - " + warning_console)

print("FIRST - TEST")
verify_errors_console()

if errors:
    print("❌ check-errors-motorsportdb")
    for err in errors:
        print("-", err)
    exit(1)
else:
    print("✅ check-errors-motorsportdb passed successfully!")