#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_URL:?FRONTEND_URL is required}"
: "${BACKEND_HEALTH_URL:?BACKEND_HEALTH_URL is required}"

echo "Purging old virtual environment folders..."
rm -rf .venv-selenium chrome-linux64 chromedriver-linux64 *.zip || true

echo "Creating clean python virtual workspace..."
python3 -m venv .venv-selenium
source .venv-selenium/bin/activate

echo "Installing Selenium..."
python3 -m pip install --upgrade pip
python3 -m pip install selenium==4.21.0 pytest

# UPGRADED TO CURL WITH RESILIENT DOWNLOADING FLAGS
echo "Downloading portable background Chrome engine..."
curl -L -o chrome-linux64.zip https://googleapis.com
curl -L -o chromedriver-linux64.zip https://googleapis.com

echo "Extracting engines..."
unzip -q chrome-linux64.zip
unzip -q chromedriver-linux64.zip

echo "Purging stale background zombie processes..."
pkill -f chromium || true
pkill -f chrome || true

echo "Launching automated end-to-end browser scenarios..."
export HEADLESS=true
python3 scripts/selenium_frontend.py
