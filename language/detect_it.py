
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = "/opt/google/chrome/chrome"

    # Priority 1: Local chromedriver (same folder as detect files)
    local_chromedriver = "/opt/render/project/src/morgan/edit/language/chromedriver"
    # Priority 2: System-wide chromedriver (fallback)
    system_chromedriver = "/usr/bin/chromedriver"

    try:
        # Try local chromedriver first
        service = Service(executable_path=local_chromedriver)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Using local chromedriver")
        return driver
    except Exception as e:
        print(f"Local chromedriver failed ({str(e)}), trying system-wide chromedriver...")
        try:
            # Fall back to system-wide chromedriver
            service = Service(executable_path=system_chromedriver)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("Using system-wide chromedriver")
            return driver
        except Exception as e:
            raise Exception(f"Both chromedrivers failed: {str(e)}")

    # If all else fails, raise an error
    raise Exception("No working chromedriver found")

def get_translation(driver, source_lang, target_lang, text):
    try:
        paragraphs = text.split('\n')
        translated_paragraphs = []
        
        for para in paragraphs:
            if not para.strip(): 
                translated_paragraphs.append('')
                continue
                
            driver.get(f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=translate")
            
            input_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Source text']")))
            input_box.clear()
            input_box.send_keys(para)
            
            # Replace time.sleep(3) with WebDriverWait for translation to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[jsname='W297wb']"))
            )
            
            translated_elements = driver.find_elements(By.CSS_SELECTOR, "span[jsname='W297wb']")
            translated_text = " ".join([el.text for el in translated_elements if el.text])
            translated_paragraphs.append(translated_text)
        
        return '\n'.join(translated_paragraphs)
    
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return text

def translate_text(text):
    driver = setup_driver()
    try:
        print("Attempting Italian → English translation...")
        return get_translation(driver, "it", "en", text)
    finally:
        driver.quit()