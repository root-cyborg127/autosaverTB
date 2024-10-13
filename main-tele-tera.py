import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Telegram bot configurations
BOT_TOKEN = "7814731853:AAHDXEkavK1cx6ZCOwa4kzPxMlAtBtwaszo"
CHAT_ID = "5127559037"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, json=payload)

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

def save_shared_file_to_terabox(driver, share_link):
    try:
        driver.get("https://www.1024terabox.com")  # Prepare the environment
        load_cookies_from_json(driver, cookies_file)
        driver.refresh()
        time.sleep(3)

        driver.get(share_link)

        # Wait for the save button to be clickable, with a timeout
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.action-bar-save.btn"))
        )

        save_button = driver.find_element(By.CSS_SELECTOR, "div.action-bar-save.btn")
        save_button.click()
        time.sleep(3)

        try:
            email_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.email-input"))
            )
            password_input = driver.find_element(By.CSS_SELECTOR, "input.pwd-input")
            login_button = driver.find_element(By.CSS_SELECTOR, "div.login-submit-btn")

            email_input.send_keys("heheboiii@tutamail.com")
            password_input.send_keys("Prachi1419")
            driver.execute_script("arguments[0].click();", login_button)
            time.sleep(2)  # Wait for possibly logging in
        except Exception:
            print("Login elements not found. Looking for an alternate 'Yes' button...")
            try:
                yes_button_alternate = driver.find_element(By.CSS_SELECTOR, "div.create-confirm.btn")
                yes_button_alternate.click()
                time.sleep(1)
            except Exception as ex:
                print(f"Alternate 'Yes' button not found. Error: {ex}")

        return True  # Success
    except Exception as e:
        print(f"Failed to save file from {share_link}. Error: {e}")
        return False  # Failure

def read_urls_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_files_from_urls(url_file, cookies_file):
    chrome_options = Options()
    # Uncomment the line below to run Chrome in headless mode
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    urls = read_urls_from_file(url_file)
    total_urls = len(urls)
    saved_count = 0

    start_time = time.time()

    for url in urls:
        success = save_shared_file_to_terabox(driver, url)
        if success:
            saved_count += 1
        
        elapsed_time = time.time() - start_time
        uptime = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        
        # Sending status update
        status_message = (
            "🚀 Terabox Upload Status 🚀\n\n"
            f"📦 Total URLs: {total_urls}\n"
            f"✅ Saved to Terabox: {saved_count}\n"
            f"💻 Active Threads: 1\n"  # Adjust as needed for threading
            f"⏳ Uptime: {uptime}\n"
            f"🔄 Status: Running smoothly"
        )
        send_telegram_message(status_message)

        time.sleep(2)  # To avoid rapid requests that might be flagged by the server
    
    driver.quit()
    print("All files processed.")

# Update these paths according to your file locations
url_file = "bigdata.txt"  # Path to your file containing URLs
cookies_file = "cookies.json"  # Path to your file containing cookies
save_files_from_urls(url_file, cookies_file)
