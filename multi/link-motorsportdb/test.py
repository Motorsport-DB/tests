from link_common import test_access, test_links_batch
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
races_path = os.path.join(BASE_PATH, "races")
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
    # Préparer toutes les URLs pour traitement par batch
    all_urls = []
    
    for driver in drivers:
        url = f"{URL}/driver.html?id={driver}"
        all_urls.append((url, "driver", driver))
    
    for team in teams:
        url = f"{URL}/team.html?id={team}"
        all_urls.append((url, "team", team))
    
    for race, year in races:
        url = f"{URL}/race.html?id={race}&year={year}"
        all_urls.append((url, "race", f"{race}/{year}"))
    
    print(f"Testing {len(all_urls)} pages for broken links in parallel...")
    
    # Traiter toutes les URLs en parallèle
    results = test_links_batch(URL, all_urls)
    
    # Regrouper les erreurs par lien cassé
    broken_links_dict = {}
    for url, page_type, identifier, broken_links in results:
        for broken_link in broken_links:
            if broken_link not in broken_links_dict:
                broken_links_dict[broken_link] = []
            broken_links_dict[broken_link].append(f"{page_type}: {identifier}")
    
    # Ajouter les erreurs regroupées
    for broken_link, sources in broken_links_dict.items():
        sources_str = ", ".join(sources[:5])  # Limite à 5 sources pour la lisibilité
        if len(sources) > 5:
            sources_str += f" ... and {len(sources) - 5} more"
        errors.append(f"[LINK-MOTORSPORTDB - BROKEN LINK] - {broken_link} (found in: {sources_str})")
        
print("FIRST - TEST")
drivers, teams, races = access_data()
first_test_total_teams = len(teams)
first_test_total_drivers = len(drivers)
first_test_total_races = len(races)
print(str(total_teams - first_test_total_teams) + " teams not pass")
print(str(total_drivers - first_test_total_drivers) + " drivers not pass")
print(str(total_races - first_test_total_races) + " races not pass")
print("SECOND - TEST")
verify_broken_link()

if errors:
    print("❌ link-motorsportdb")
    for err in errors:
        print("-", err)
    exit(1)
else:
    print("✅ link-motorsportdb passed successfully!")