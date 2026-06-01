#!/usr/bin/env bash
set -euo pipefail

cd client

echo "Installing frontend dependencies..."
# --legacy-peer-deps is used to bypass peer dependency conflicts that may arise with newer versions of npm.
npm install --legacy-peer-deps


echo "Running frontend dependency security scan..."
npm audit --audit-level=critical

echo "Running frontend lint checks if available..."
npm run lint --if-present

echo "Building frontend..."
npm run build
