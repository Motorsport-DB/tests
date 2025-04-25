import requests
import json
import os

FILE = "/cards.json"

def generate_cards(url):
    url = url + "/assets/php/generate_index_cards.php?id=0"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Cartes générées avec succès.")
            return True if (response.json()) else False
        else:
            print(f"Erreur lors de la génération des cartes : Code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print("Erreur lors de la requête pour générer les cartes :", e)
        return None

def get_url_from_config():
    config_path = os.path.join(os.path.dirname(__file__), "../../config.json")
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            url = config.get("URL_LOCAL_TEST")
            if url and not url.startswith(("http://", "https://")):
                url = "http://" + url  # Add default protocol if missing
            return url
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Erreur lors de la lecture du fichier de configuration :", e)
        return None

def test_server_response(url):
    if not url:
        print("Test échoué : impossible de récupérer l'URL depuis le fichier de configuration.")
        exit(2)

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
    url = get_url_from_config()
    
    if (not test_server_response(url)): # FIRST TEST SHOULD BE FALSE
        generate_cards(url)
        if (test_server_response(url)):
            print("✅ retrieve-cards-motorsportdb passed successfully!")
        else:
            print("❌ retrieve-cards-motorsportdb")
            exit(1)
    else:
        print("⚠️ retrieve-cards-motorsportdb first test should be false...")