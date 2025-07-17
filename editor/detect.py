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
    service = Service(executable_path='editor/chromedriver.exe')
    return webdriver.Chrome(service=service, options=chrome_options)

def get_translation(driver, source_lang, target_lang, text):
    try:
        driver.get(f"https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=translate")
        
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Source text']")))
        input_box.clear()
        input_box.send_keys(text)
        
        time.sleep(3)
        
        translated_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span[jsname='W297wb']"))
        )
        
        return " ".join([el.text for el in translated_elements if el.text])
    
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