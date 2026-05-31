#!/usr/bin/env bash
set -euo pipefail

cd client

echo "Installing frontend dependencies..."
npm install

echo "Running frontend dependency security scan..."
npm audit --audit-level=critical

echo "Running frontend lint checks if available..."
npm run lint --if-present

echo "Building frontend..."
npm run build
