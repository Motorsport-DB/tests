import os

def check_unused_picture(pictures, json_directory):
    errors = []

    for image_name in pictures:
        if ("default" == image_name):
            continue # Prevent default image to cause an error
        json_file_path = os.path.join(json_directory, f"{image_name}.json")
        if not os.path.isfile(json_file_path):
            errors.append(f"L'image '{image_name}' n'est rattachée à aucun fichier JSON.")
    
    return errors

def check_unused_picture_directory(pictures, directory):
    errors = []

    for image_name in pictures:
        if image_name == "default":
            continue  # Skip the default image
        folder_path = os.path.join(directory, image_name)
        if not os.path.isdir(folder_path):
            errors.append(f"L'image '{image_name}' ne correspond à aucun dossier dans le répertoire '{directory}'.")
    
    return errors