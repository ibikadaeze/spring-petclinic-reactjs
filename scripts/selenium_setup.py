#!/usr/bin/env python3
"""Setup and run Selenium E2E tests."""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run command and exit on failure."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: {description} failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def cleanup_venv():
    """Clean up old virtual environments and browser files."""
    print("Purging old virtual environment folders...")
    paths = [".venv-selenium", "chrome-linux64", "chromedriver-linux64"]
    for path in paths:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)

    for zip_file in Path(".").glob("*.zip"):
        zip_file.unlink()

def main():
    frontend_url = os.environ.get("FRONTEND_URL")
    backend_health_url = os.environ.get("BACKEND_HEALTH_URL")

    if not frontend_url or not backend_health_url:
        print("ERROR: FRONTEND_URL and BACKEND_HEALTH_URL environment variables required")
        sys.exit(1)

    cleanup_venv()

    print("Creating clean python virtual workspace...")
    subprocess.run("python3 -m venv .venv-selenium", shell=True, check=True)

    print("Installing Selenium and Automated Driver Managers...")
    run_command(
        ".venv-selenium/bin/python3 -m pip install --upgrade pip",
        "Upgrading pip"
    )
    run_command(
        ".venv-selenium/bin/pip install selenium==4.21.0 webdriver-manager pytest",
        "Installing test dependencies"
    )

    # Kill stale processes
    print("Purging stale background zombie processes...")
    subprocess.run("pkill -f chromium || true", shell=True)
    subprocess.run("pkill -f chrome || true", shell=True)

    print("Launching automated end-to-end browser scenarios...")
    os.environ["HEADLESS"] = "true"
    os.environ["FRONTEND_URL"] = frontend_url
    os.environ["BACKEND_HEALTH_URL"] = backend_health_url

    # Run tests
    run_command(
        f".venv-selenium/bin/python3 scripts/selenium_frontend.py",
        "Running Selenium tests"
    )

    print("\n✓ Selenium E2E tests completed successfully!")

if __name__ == "__main__":
    main()
