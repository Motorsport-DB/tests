"""
Fonctions communes pour la validation des photos et pays manquants.
"""
import json
import os

# Extensions d'images supportées
IMAGE_EXTENSIONS = ['.jpg', '.png']

# Dossiers à ignorer
IGNORED_FOLDERS = ['__pycache__', '.git', '.vscode']

def check_image_exists(identifier, assets_path):
    """Vérifie si une image existe pour l'entité donnée."""
    base_folder = os.path.join(assets_path, "other")
    
    if not os.path.exists(base_folder):
        return False
    
    # Chercher n'importe quelle image avec le nom de l'identifiant
    for ext in IMAGE_EXTENSIONS:
        if os.path.exists(os.path.join(base_folder, f"{identifier}{ext}")):
            return True
    
    return False

def validate_drivers(drivers_path, assets_path):
    """Valide les drivers pour photos et pays manquants."""
    warnings = []
    
    if not os.path.exists(drivers_path):
        return [f"Driver path not found: {drivers_path}"]
    
    driver_files = [f for f in os.listdir(drivers_path) 
                   if f.endswith(".json") and not os.path.isdir(os.path.join(drivers_path, f))]
    
    for driver_file in driver_files:
        driver_id = driver_file.replace(".json", "")
        file_path = os.path.join(drivers_path, driver_file)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Check for missing photo
            if not check_image_exists(driver_id, assets_path):
                warnings.append(f"[DRIVER-PHOTO] {driver_id}: No photo found")
            
            # Check for missing country
            if "country" not in data or not data["country"] or data["country"].strip() == "":
                warnings.append(f"[DRIVER-COUNTRY] {driver_id}: No country specified")
        
        except Exception as e:
            warnings.append(f"[DRIVER-ERROR] {driver_id}: Error reading file - {e}")
    
    return warnings

def validate_teams(teams_path, assets_path):
    """Valide les teams pour photos et pays manquants."""
    warnings = []
    
    if not os.path.exists(teams_path):
        return [f"Team path not found: {teams_path}"]
    
    team_files = [f for f in os.listdir(teams_path) 
                 if f.endswith(".json") and not os.path.isdir(os.path.join(teams_path, f))]
    
    for team_file in team_files:
        team_id = team_file.replace(".json", "")
        file_path = os.path.join(teams_path, team_file)
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Check for missing photo
            if not check_image_exists(team_id, assets_path):
                warnings.append(f"[TEAM-PHOTO] {team_id}: No photo found")
            
            # Check for missing country
            if "country" not in data or not data["country"] or data["country"].strip() == "":
                warnings.append(f"[TEAM-COUNTRY] {team_id}: No country specified")
        
        except Exception as e:
            warnings.append(f"[TEAM-ERROR] {team_id}: Error reading file - {e}")
    
    return warnings

def validate_championships(races_path, assets_path):
    """Valide les championships pour photos manquantes."""
    warnings = []
    
    if not os.path.exists(races_path):
        return [f"Races path not found: {races_path}"]
    
    championships = [d for d in os.listdir(races_path) 
                    if os.path.isdir(os.path.join(races_path, d)) and d not in IGNORED_FOLDERS]
    
    for championship_id in championships:
        # Check for missing photo
        if not check_image_exists(championship_id, assets_path):
            warnings.append(f"[CHAMPIONSHIP-PHOTO] {championship_id}: No photo found")
    
    return warnings
