import requests
import json
import os

FILE = "/cards.json"

def get_url_from_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            return config.get("URL_LOCAL_TEST")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Erreur lors de la lecture du fichier de configuration :", e)
        return None

def test_server_response():
    url = get_url_from_config()
    if not url:
        print("Test échoué : impossible de récupérer l'URL depuis le fichier de configuration.")
        return False

    url = url + FILE
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print("Test échoué : le serveur a répondu avec un code 404.")
            return False
        else:
            print("Test réussi : le serveur a répondu avec un code", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Test échoué : une erreur s'est produite lors de la requête.", e)
        return False
    return True

if __name__ == "__main__":
    if (test_server_response()):
        print("✅ retrieve-cards-motorsportdb passed successfully!")
    else:
        print("❌ retrieve-cards-motorsportdb")
        exit(1)