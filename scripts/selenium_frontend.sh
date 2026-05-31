#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_URL:?FRONTEND_URL is required}"
: "${BACKEND_HEALTH_URL:?BACKEND_HEALTH_URL is required}"

python3 -m venv .venv-selenium
. .venv-selenium/bin/activate

python -m pip install --upgrade pip
python -m pip install selenium

python scripts/selenium_frontend.py
