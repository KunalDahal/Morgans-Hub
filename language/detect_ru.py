
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import undetected_chromedriver as uc

def setup_driver():
    chrome_binary = "/opt/render/project/src/chrome/chrome-linux64/chrome"
    chromedriver_path = "/opt/render/project/src/morgan/edit/language/chromedriver"

    if os.path.exists(chromedriver_path) and os.access(chromedriver_path, os.X_OK):
        print("Using local ChromeDriver")

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1200,800")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = chrome_binary

        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        print("Local ChromeDriver not found or not executable. Using undetected-chromedriver fallback.")
        driver = uc.Chrome(
            headless=True,
            version_main=138,  # Match your downloaded Chrome version
            browser_executable_path=chrome_binary
        )

    return driver

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
        print("Attempting Russian → English translation...")
        return get_translation(driver, "ru", "en", text)
    finally:
        driver.quit()