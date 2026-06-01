#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_URL:?FRONTEND_URL is required}"
: "${BACKEND_HEALTH_URL:?BACKEND_HEALTH_URL is required}"

echo "Purging old virtual environment folders to secure clean runs..."
rm -rf .venv-selenium

echo "Creating clean python virtual workspace..."
python3 -m venv .venv-selenium

echo "Activating workspace environment..."
source .venv-selenium/bin/activate

echo "Upgrading package pip installers..."
python3 -m pip install --upgrade pip

echo "Installing Selenium functional browser automation dependencies..."
python3 -m pip install selenium pytest

echo "Launching automated end-to-end browser scenarios..."
# Setting environment variable for headless run just in case your python script looks for it
export HEADLESS=true 
python3 scripts/selenium_frontend.py
