from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess 
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--remote-debugging-port=0")  
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Updated paths
    chrome_options.binary_location = "/usr/local/bin/chrome/chrome"
    chromedriver_path = "/usr/local/bin/chromedriver"

    # Verify paths exist
    if not os.path.exists(chrome_options.binary_location):
        raise FileNotFoundError(f"Chrome binary not found at {chrome_options.binary_location}")
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

    print("ChromeDriver version:", subprocess.getoutput(f"{chromedriver_path} --version"))

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("✅ ChromeDriver started successfully")
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
        print("Attempting Italian → English translation...")
        return get_translation(driver, "it", "en", text)
    finally:
        driver.quit()
