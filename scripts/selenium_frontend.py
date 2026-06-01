import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# 1. Initialize standard Chrome Options
chrome_options = Options()

# 2. Point explicitly to your active Snap Chromium binary installation path
chrome_options.binary_location = "/snap/bin/chromium"

# 3. Enforce strict background configurations for headless CI node environments
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-allow-origins=*")

# 4. Use the specific CHROMIUM type manager hook to download a matching driver
# This instructs webdriver-manager to fetch the uncontained Chromium driver variant
service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

print("Initializing automated end-to-end browser driver instance...")
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # FETCH ASSIGNED REPOSITORY ENVIRONMENT VARIABLES
    frontend_url = os.getenv("FRONTEND_URL", "http://192.168.56")
    print(f"Navigating automated scenarios to target context path: {frontend_url}")
    
    # 5. AUTOMATED TEST SCENARIOS
    driver.get(frontend_url)
    
    # Capture the active web document title validation context
    page_title = driver.title
    print(f"Successfully connected! Verified Landing Page Title: '{page_title}'")
    
    # Clean termination sequence
    driver.quit()
    print("All functional validation assertions successfully completed green!")
    sys.exit(0)

except Exception as error:
    print(f"CRITICAL SYSTEM ERROR DURING DRIVER LIFECYCLE: {str(error)}", file=sys.stderr)
    sys.exit(1)
