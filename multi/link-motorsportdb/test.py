from link_common import test_access, test_links  
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
races_path = os.path.expanduser("~/clone-motorsportdb/races")
drivers = [f.split('/')[-1].strip().replace(".json","") for f in drivers_files]
teams = [f.split('/')[-1].strip().replace(".json","") for f in teams_files]

races = []
for championship in os.listdir(races_path):
    championship_path = os.path.join(races_path, championship)
    if os.path.isdir(championship_path):
        for race_file in os.listdir(championship_path):
            if race_file.endswith(".json"):
                race_year = race_file.replace(".json", "")
                races.append((championship, race_year))
                
                
total_drivers = len(drivers)
total_teams = len(teams)
total_races = len(races)

def access_data():
    drivers_valid = []
    teams_valid = []
    races_valid = []
    for driver in drivers:
        if (driver == ""):
            continue
        url = f"{URL}/getDrivers.php?id={driver}"
        isValid = test_access(url)
        if (isValid):
            drivers_valid.append(driver)
        else:
            errors.append(f"[LINK-MOTORSPORTDB - ACCESS] - (driver) Can't access to {url}")
    
    for team in teams:
        if (team == ""):
            continue
        url = f"{URL}/getTeams.php?id={team}"
        isValid = test_access(url)
        if (isValid):
            teams_valid.append(team)
        else:
            errors.append(f"[LINK-MOTORSPORTDB - ACCESS] - (team) Can't access to {url}")
    
    for race, year in races:
        if (race == ""):
            continue
        url = f"{URL}/getRaces.php?id={race}&year={year}"
        isValid = test_access(url)
        if (isValid):
            races_valid.append((race, year))
        else:
            errors.append(f"[LINK-MOTORSPORTDB - ACCESS] - (race) Can't access to {url}")
    
    return drivers_valid, teams_valid, races_valid

def verify_broken_link():
    for i in range(len(drivers)):
        print("["+str(i)+"/"+str(len(drivers))+"]" + "Testing: "+ str(drivers[i]))
        url = f"{URL}/driver.html?id={drivers[i]}"
        broken_links = test_links(URL, url)       
        for broken_link in broken_links:
            errors.append(f"[LINK-MOTORSPORTDB - BROKEN LINK] - ({drivers[i]}) Broken link in {url} at {broken_link}")
    
    for i in range(len(teams)):
        print("["+str(i)+"/"+str(len(teams))+"]" + "Testing: "+ str(teams[i]))
        url = f"{URL}/team.html?id={teams[i]}"
        broken_links = test_links(URL, url)
        for broken_link in broken_links:
            errors.append(f"[LINK-MOTORSPORTDB - BROKEN LINK] - ({teams[i]}) Broken link in {url} at {broken_link}")
    
    for i in range(len(races)):
        race, year = races[i]
        print("["+str(i)+"/"+str(len(races))+"]" + "Testing: "+ str(races[i]))
        url = f"{URL}/race.html?id={race}&year={year}"
        broken_links = test_links(URL, url)
        for broken_link in broken_links:
            errors.append(f"[LINK-MOTORSPORTDB - BROKEN LINK] - ({race},{year}) Broken link in {url} at {broken_link}")
        
print("FIRST - TEST")
drivers, teams, races = access_data()
first_test_total_teams = len(teams)
first_test_total_drivers = len(drivers)
first_test_total_races = len(races)
print(str(total_teams - first_test_total_teams) + " teams not pass")
print(str(total_drivers - first_test_total_drivers) + " drivers not pass")
print(str(total_races - first_test_total_races) + " teams not pass")
print("SECOND - TEST")
verify_broken_link()

if errors:
    print("❌ link-motorsportdb")
    for err in errors:
        print("-", err)
    exit(1)
else:
    print("✅ link-motorsportdb passed successfully!")