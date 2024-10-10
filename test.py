from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

visited_urls = set()  # Track visited URLs

def load_cookies_from_json(driver, cookies_file):
    try:
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                if 'sameSite' in cookie:
                    del cookie['sameSite']
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print(f"Cookies file {cookies_file} not found.")
    except Exception as e:
        print(f"Error loading cookies: {e}")

def save_shared_file_to_terabox(share_link, cookies_file):
    # Each thread needs its own WebDriver instance
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    if share_link not in visited_urls:  # Check if the URL has been processed
        visited_urls.add(share_link)  # Mark the URL as visited
        driver.get("https://www.1024terabox.com")
        load_cookies_from_json(driver, cookies_file)
        driver.refresh()
        time.sleep(3)

        driver.get(share_link)
        time.sleep(3)

        try:
            save_button = driver.find_element(By.CSS_SELECTOR, "div.action-bar-save.btn")
            save_button.click()
            time.sleep(10)  # Adjust timing based on the expected page load time
            
            
            print(f"File from {share_link} saved successfully.")
        except Exception as e:
            print(f"Failed to save file from {share_link}. Error: {e}")
        finally:
            driver.quit()
    else:
        print(f"URL {share_link} has been already visited.")

def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_files_from_urls_concurrently(url_file, cookies_file):
    urls = read_urls_from_file(url_file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(save_shared_file_to_terabox, url, cookies_file) for url in urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing URL: {str(e)}")

# Update these to your file locations
url_file = "urls.txt"
cookies_file = "cookies.json"
save_files_from_urls_concurrently(url_file, cookies_file)