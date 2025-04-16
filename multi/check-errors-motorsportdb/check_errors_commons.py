from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def check_console_errors(link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    driver = webdriver.Chrome(options=chrome_options)

    console_errors = []
    console_warnings = []

    try:
        driver.get(link)
        time.sleep(2)  # Laisse le JS charger

        logs = driver.get_log("browser")
        for entry in logs:
            msg = entry["message"]
            level = entry["level"]

            # Filtrage des erreurs non bloquantes connues
            if "favicon.ico" in msg and "404" in msg:
                console_warnings.append(msg)
                continue

            if level == "SEVERE":
                console_errors.append(msg)

    except Exception as e:
        console_errors.append(f"[ERROR] Could not open page: {e}")

    finally:
        driver.quit()

    return console_errors, console_warnings
