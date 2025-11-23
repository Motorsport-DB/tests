from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Thread-local storage for WebDriver instances
thread_local = threading.local()

# Cache global pour les liens testés
link_cache = {}
link_cache_lock = threading.Lock()

# Configuration de Selenium (headless Chrome)
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=chrome_options)

def get_driver():
    """Récupère ou crée un WebDriver pour le thread actuel."""
    if not hasattr(thread_local, "driver") or thread_local.driver is None:
        thread_local.driver = create_driver()
    return thread_local.driver

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
    driver = get_driver()

    try:
        driver.get(link)
        time.sleep(0.5)
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

            # Ignore les ancres, liens externes et fichiers PHP
            if test_link.startswith("#") or "http" in test_link or test_link.endswith(".php") or ".php?" in test_link:
                continue

            test_url = f"{BASE_URL}/{test_link}".replace("//", "/").replace(":/", "://")

            # Vérifier le cache
            with link_cache_lock:
                if test_url in link_cache:
                    if not link_cache[test_url]:
                        broken_links.append(test_url)
                    continue

            try:
                driver.get(test_url)
                time.sleep(0.5)

                is_broken = driver.find_elements(By.ID, "text_error")
                
                with link_cache_lock:
                    link_cache[test_url] = not is_broken
                
                if is_broken:
                    broken_links.append(test_url)
            except Exception as e:
                print(f"[BROKEN_LINK] Exception for {test_url}: {e}")
                broken_links.append(test_url)
                with link_cache_lock:
                    link_cache[test_url] = False

    except Exception as e:
        print(f"[ERROR] Main page load failed: {e}")
        return ["Unknown error..."]

    return broken_links


def test_links_batch(BASE_URL, urls_data, max_workers=10):
    """Teste plusieurs pages en parallèle.
    
    Args:
        BASE_URL: URL de base du site
        urls_data: Liste de tuples (url, type, identifier)
        max_workers: Nombre de threads parallèles
    
    Returns:
        Liste de tuples (url, type, identifier, broken_links)
    """
    results = []
    total = len(urls_data)
    processed = 0
    processed_lock = threading.Lock()
    
    def process_url(url_tuple):
        nonlocal processed
        url, page_type, identifier = url_tuple
        broken_links = test_links(BASE_URL, url)
        
        with processed_lock:
            processed += 1
            if processed % 50 == 0 or processed == total:
                print(f"Progress: {processed}/{total} pages tested")
        
        return (url, page_type, identifier, broken_links)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_url, url_data) for url_data in urls_data]
        
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing URL: {e}")
    
    return results