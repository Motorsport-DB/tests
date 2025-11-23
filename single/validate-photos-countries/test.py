"""
Test de validation pour vérifier les photos et pays manquants.
Ce test génère des WARNINGS (pas des erreurs).
"""
import os
import json
from validate_common import validate_drivers, validate_teams, validate_championships

def get_config():
    """Charge la configuration depuis config.json."""
    config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def validate_all():
    """Valide toutes les entités pour photos et pays manquants."""
    config = get_config()
    
    base_path = os.path.expanduser(config.get("LINUX_URL_LOCAL_FILES"))
    drivers_path = os.path.join(base_path, "drivers")
    teams_path = os.path.join(base_path, "teams")
    races_path = os.path.join(base_path, "races")
    
    # Le path assets est relatif au repo principal
    assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../assets"))
    
    all_warnings = []
    
    print("Validating drivers...")
    all_warnings.extend(validate_drivers(drivers_path, assets_path))
    
    print("Validating teams...")
    all_warnings.extend(validate_teams(teams_path, assets_path))
    
    print("Validating championships...")
    all_warnings.extend(validate_championships(races_path, assets_path))
    
    return all_warnings

def print_summary(warnings):
    """Affiche un résumé des warnings."""
    if not warnings:
        print("\n✅ No missing photos or countries found!")
        return
    
    # Grouper par catégorie
    categories = {
        "DRIVER-PHOTO": [],
        "DRIVER-COUNTRY": [],
        "TEAM-PHOTO": [],
        "TEAM-COUNTRY": [],
        "CHAMPIONSHIP-PHOTO": []
    }
    
    for warning in warnings:
        for category in categories.keys():
            if category in warning:
                categories[category].append(warning)
                break
    
    print("\n" + "="*70)
    print("VALIDATION SUMMARY - MISSING PHOTOS & COUNTRIES")
    print("="*70)
    
    for category, warns in categories.items():
        if warns:
            print(f"\n{category} ({len(warns)} issues):")
            for w in warns:
                print(f"  ⚠️  {w}")
    
    print("\n" + "="*70)
    print(f"Total warnings: {len(warnings)}")
    print("="*70 + "\n")

if __name__ == "__main__":
    print("Starting validation for missing photos and countries...\n")
    
    all_warnings = validate_all()
    print_summary(all_warnings)
    
    print("ℹ️  Note: These are warnings only, not errors.")
    # Exit code 0 car ce ne sont que des warnings
    exit(0)
