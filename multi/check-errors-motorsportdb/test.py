from check_errors_commons import check_console_errors
import os

URL = "http://192.168.1.33:8043"

errors = []

# Get all drivers and teams
drivers_files = [
    f for f in os.listdir(os.path.expanduser("~/clone-motorsportdb/drivers"))
    if f.endswith(".json")
]
teams_files = [
    f for f in os.listdir(os.path.expanduser("~/clone-motorsportdb/teams"))
    if f.endswith(".json")
]
races_files = []
races_path = os.path.expanduser("~/clone-motorsportdb/races")

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
    for i in range(len(drivers)):
        print("["+str(i)+"/"+str(len(drivers))+"] " + "Testing: "+ str(drivers[i]))
        url = f"{URL}/driver.html?id={drivers[i]}"
        errors_console, warnings_console = check_console_errors(url)       
        for error_console in errors_console:
            errors.append(f"[CHECK-ERRORS-MOTORSPORTDB - BROKEN LINK] - ({drivers[i]}) errors in {url} = {error_console}")
        for warning_console in warnings_console:
            print(f"[⚠️] - " + warning_console)
    
    for i in range(len(teams)):
        print("["+str(i)+"/"+str(len(teams))+"] " + "Testing: "+ str(teams[i]))
        url = f"{URL}/team.html?id={teams[i]}"
        errors_console, warnings_console = check_console_errors(url)
        for error_console in errors_console:
            errors.append(f"[CHECK-ERRORS-MOTORSPORTDB - BROKEN LINK] - ({teams[i]}) errors in {url} = {error_console}")
        for warning_console in warnings_console:
            print(f"[⚠️] - " + warning_console)

    for i in range(len(races_files)):
        championship, year = races_files[i]
        print(f"[{i}/{len(races_files)}] Testing: Championship={championship}, Year={year}")
        url = f"{URL}/race.html?id={championship}&year={year}"
        errors_console, warnings_console = check_console_errors(url)
        for error_console in errors_console:
            errors.append(f"[CHECK-ERRORS-MOTORSPORTDB - BROKEN LINK] - ({races_files[i]}) errors in {url} = {error_console}")
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