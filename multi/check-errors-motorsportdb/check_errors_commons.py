from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread-local storage for WebDriver instances
thread_local = threading.local()

def get_driver():
    """Get or create a WebDriver for the current thread"""
    if not hasattr(thread_local, 'driver'):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
        thread_local.driver = webdriver.Chrome(options=chrome_options)
    return thread_local.driver

def close_driver():
    """Close the WebDriver for the current thread"""
    if hasattr(thread_local, 'driver'):
        thread_local.driver.quit()
        delattr(thread_local, 'driver')

def check_console_errors(link):
    console_errors = []
    console_warnings = []

    try:
        driver = get_driver()
        driver.get(link)
        time.sleep(1)  # Reduced from 2 to 1 second

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

    return console_errors, console_warnings

def check_console_errors_batch(urls, max_workers=10):
    """Check console errors for multiple URLs in parallel
    
    Args:
        urls: List of tuples (url, page_type, identifier)
        max_workers: Maximum number of parallel workers (default: 10)
    
    Returns:
        List of tuples (url, page_type, identifier, errors_console, warnings_console)
    """
    results = []
    
    def check_url(url_tuple):
        url, page_type, identifier = url_tuple
        try:
            errors_console, warnings_console = check_console_errors(url)
            return (url, page_type, identifier, errors_console, warnings_console)
        except Exception as e:
            return (url, page_type, identifier, [f"Exception: {e}"], [])
        finally:
            # Clean up driver periodically to avoid memory issues
            pass
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_url, url_tuple): url_tuple for url_tuple in urls}
        
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    
    # Clean up all drivers after batch processing
    close_driver()
    
    return results
