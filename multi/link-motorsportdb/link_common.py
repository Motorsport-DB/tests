from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests

# Configuration de Selenium (headless Chrome)
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def test_access(link):
    try:
        res = requests.get(link, timeout=5)
        if 200 != res.status_code:
            return False
    except Exception as e:
        print(f"[ERROR] Access issue: {e}")
        return False
    return True


# Test des liens internes d'une page donnée
def test_links(BASE_URL, link):
    broken_links = []
    driver = create_driver()

    try:
        driver.get(link)
        time.sleep(1)
        if "404" in driver.title or driver.find_elements(By.ID, "text_error"):
            return ["Unable to access..."]

        soup = BeautifulSoup(driver.page_source, "html.parser")
        tested_links = []
        for a in soup.find_all("a", href=True):
            if a['href'] not in tested_links:
                tested_links.append(a['href'])
            else:
                continue
            test_link = a['href']

            # Ignore les ancres ou liens externes
            if test_link.startswith("#") or "http" in test_link:
                continue

            test_url = f"{BASE_URL}/{test_link}".replace("//", "/").replace(":/", "://")

            try:
                driver.get(test_url)
                time.sleep(1)

                if driver.find_elements(By.ID, "text_error"):
                    broken_links.append(test_url)
            except Exception as e:
                print(f"[BROKEN_LINK] Exception for {test_url}: {e}")
                broken_links.append(test_url)

    except Exception as e:
        print(f"[ERROR] Main page load failed: {e}")
        return ["Unknown error..."]

    finally:
        driver.quit()

    return broken_links