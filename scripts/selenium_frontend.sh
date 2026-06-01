#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_URL:?FRONTEND_URL is required}"
: "${BACKEND_HEALTH_URL:?BACKEND_HEALTH_URL is required}"

echo "Purging old virtual environment folders..."
rm -rf .venv-selenium chrome-linux64 chromedriver-linux64 *.zip || true

echo "Creating clean python virtual workspace..."
python3 -m venv .venv-selenium
source .venv-selenium/bin/activate

echo "Installing Selenium and Automated Driver Managers..."
python3 -m pip install --upgrade pip
# ADDED webdriver-manager HERE
python3 -m pip install selenium==4.21.0 webdriver-manager pytest

echo "Purging stale background zombie processes..."
pkill -f chromium || true
pkill -f chrome || true

echo "Launching automated end-to-end browser scenarios..."
export HEADLESS=true
python3 scripts/selenium_frontend.py
