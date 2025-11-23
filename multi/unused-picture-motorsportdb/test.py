import os
import json
from unused_picture_common import check_unused_picture, check_unused_picture_directory

# Load config
config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
with open(config_path, "r") as f:
    config = json.load(f)

BASE_PATH = os.path.expanduser(config.get("LINUX_URL_LOCAL_FILES", "~/clone-motorsportdb"))

def test_unattached_driver_images():
    drivers_images_dir = os.path.join(BASE_PATH, "drivers", "picture")
    drivers_dir = os.path.join(BASE_PATH, "drivers")
    teams_images_dir = os.path.join(BASE_PATH, "teams", "picture")
    teams_dir = os.path.join(BASE_PATH, "teams")
    races_images_dir = os.path.join(BASE_PATH, "races", "picture")
    races_dir = os.path.join(BASE_PATH, "races")

    try:
        drivers_images = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(drivers_images_dir)
            if os.path.isfile(os.path.join(drivers_images_dir, filename))
        ]
        teams_images = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(teams_images_dir)
            if os.path.isfile(os.path.join(teams_images_dir, filename))
        ]
        races_images = [
            os.path.splitext(filename)[0]
            for filename in os.listdir(races_images_dir)
            if os.path.isfile(os.path.join(races_images_dir, filename))
        ]
    except Exception as e:
        print("Le répertoire d'image n'existe peut-être pas.\nIl ne faut pas lancer les scripts en tant que root")
        print(e)
        exit(404)
    errors = []
    
    errors.extend(check_unused_picture(drivers_images, drivers_dir))
    errors.extend(check_unused_picture(teams_images, teams_dir))
    errors.extend(check_unused_picture_directory(races_images, races_dir))
    
    if errors:
        print("❌ unused-picture-motorsportdb")
        for err in errors:
            print("-", err)
        exit(1)
    else:
        print("✅ unused-picture-motorsportdb passed successfully!")

if __name__ == "__main__":
    test_unattached_driver_images()