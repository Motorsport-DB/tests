import requests
import time
import random

def check_site_availability(url, max_attempts=30):
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("Success: Le site est disponible.")
                return
        except requests.exceptions.RequestException:
            pass  # Ignorer les erreurs et continuer les tentatives

        attempts += 1
        wait_time = random.uniform(1, 5)  # Temps d'attente aléatoire entre 1 et 5 secondes
        time.sleep(wait_time)

    print("Erreur: Website is not available after 30 attempts.")
    exit(2)

if __name__ == "__main__":
    url = "http://192.168.1.33:8043"
    check_site_availability(url)