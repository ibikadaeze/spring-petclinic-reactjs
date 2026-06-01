#!/usr/bin/env python3
import os
import sys
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Instantiate specialized Chromium configurations
chromium_options = ChromiumOptions()

# 2. Hardcode the absolute executable binary location mapping to Snap
chromium_options.binary_location = "/snap/bin/chromium"

# 3. Apply standard background processing parameters for headless environments
chromium_options.add_argument("--headless=new")
chromium_options.add_argument("--no-sandbox")
chromium_options.add_argument("--disable-dev-shm-usage")
chromium_options.add_argument("--remote-allow-origins=*")

# 4. Initialize using explicit binary binding
driver = webdriver.Chrome(options=chromium_options)

def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


def main():
    frontend_url = require_env("FRONTEND_URL")
    backend_health_url = require_env("BACKEND_HEALTH_URL")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print(f"Opening frontend: {frontend_url}")
        driver.get(frontend_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        title = driver.title
        body_text = driver.find_element(By.TAG_NAME, "body").text

        if not body_text.strip():
            raise RuntimeError("Frontend loaded, but the page body is empty")

        print(f"Frontend page title: {title}")
        print("Frontend page loaded successfully")

        print(f"Opening backend health endpoint: {backend_health_url}")
        driver.get(backend_health_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        health_body = driver.find_element(By.TAG_NAME, "body").text

        if "UP" not in health_body:
            raise RuntimeError(f"Backend health check did not report UP: {health_body}")

        print("Backend health endpoint is reachable from browser session")
    finally:
        driver.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
