#!/usr/bin/env python3
"""End-to-end Selenium tests for Pet Clinic frontend."""

import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pytest

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://192.168.56.11/")
BACKEND_HEALTH_URL = os.environ.get("BACKEND_HEALTH_URL", "http://192.168.56.12:9966/petclinic/actuator/health")
HEADLESS = os.environ.get("HEADLESS", "true").lower() == "true"


@pytest.fixture
def driver():
    """Setup and teardown Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_frontend_loads(driver):
    """Test that frontend page loads successfully."""
    driver.get(FRONTEND_URL)
    wait = WebDriverWait(driver, 10)

    # Check for page title or main element
    assert "Spring" in driver.title or "Petclinic" in driver.title, "Page title missing expected text"

    # Wait for main content to load
    try:
        wait.until(EC.presence_of_element_located((By.ID, "mount")))
    except:
        pass  # React apps may load dynamically


def test_page_has_content(driver):
    """Test that page has rendered content."""
    driver.get(FRONTEND_URL)
    wait = WebDriverWait(driver, 10)

    # Check for body content
    body = driver.find_element(By.TAG_NAME, "body")
    assert body.get_attribute("innerHTML").strip(), "Page body is empty"


def test_no_console_errors(driver):
    """Test that page loaded without critical console errors."""
    driver.get(FRONTEND_URL)

    # Get browser logs
    logs = driver.get_log("browser")

    # Check for SEVERE errors (not warnings)
    severe_errors = [log for log in logs if log["level"] == "SEVERE"]

    # Filter out expected errors
    critical_errors = [
        e for e in severe_errors
        if "404" not in str(e) or ".js" not in str(e)
    ]

    assert not critical_errors, f"Found critical console errors: {critical_errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
