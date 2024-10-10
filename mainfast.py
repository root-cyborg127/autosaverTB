from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

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

def save_shared_file_to_terabox(driver, share_link, cookies_file):
    driver.get("https://www.1024terabox.com")  # Prepare the environment
    load_cookies_from_json(driver, cookies_file)
    driver.refresh()
    time.sleep(3)

    driver.get(share_link)
    time.sleep(3)

    try:
        save_button = driver.find_element(By.CSS_SELECTOR, "div.action-bar-save.btn")
        save_button.click()
        time.sleep(3)
        
        try:
            # Attempt to fill login if required
            email_input = driver.find_element(By.CSS_SELECTOR, "input.email-input")
            password_input = driver.find_element(By.CSS_SELECTOR, "input.pwd-input")
            login_button = driver.find_element(By.CSS_SELECTOR, "div.login-submit-btn")
            
            email_input.send_keys("heheboiii@tutamail.com")
            password_input.send_keys("Prachi1419")
            driver.execute_script("arguments[0].click();", login_button)
            time.sleep(2)  # Wait for possibly logging in
        except Exception as e:
            # Handling the scenario where login elements are not found
            print("Login elements not found. Looking for an alternate 'Yes' button...")
            try:
                yes_button_alternate = driver.find_element(By.CSS_SELECTOR, "div.create-confirm.btn")
                yes_button_alternate.click()
                time.sleep(1)
            except Exception as ex:
                print(f"Alternate 'Yes' button not found. Error: {ex}")
        
        print(f"File from {share_link} saved successfully.")
    except Exception as e:
        print(f"Failed to save file from {share_link}. Error: {e}")
        print("Debug Info:", driver.page_source)

def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_files_from_urls(url_file, cookies_file):
    chrome_options = Options()
    # Uncomment the line below to run Chrome in headless mode
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    urls = read_urls_from_file(url_file)
    
    for url in urls:
        save_shared_file_to_terabox(driver, url, cookies_file)
        time.sleep(2)  # To avoid rapid requests that might be flagged by the server
    
    driver.quit()
    print("All files processed.")

# Update these paths according to your file locations
url_file = "bigdata.txt"  # Path to your file containing URLs
cookies_file = "cookies.json"  # Path to your file containing cookies
save_files_from_urls(url_file, cookies_file)