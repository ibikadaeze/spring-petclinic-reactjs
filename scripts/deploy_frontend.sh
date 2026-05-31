#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_HOST:?FRONTEND_HOST is required}"
: "${FRONTEND_USER:?FRONTEND_USER is required}"

echo "Packaging frontend build..."
tar -czf frontend-build.tar.gz -C client/build .

echo "Copying frontend build to ${FRONTEND_HOST}..."
scp frontend-build.tar.gz "${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/frontend-build.tar.gz"

echo "Deploying frontend build to Nginx..."
ssh "${FRONTEND_USER}@${FRONTEND_HOST}" "
  sudo rm -rf /var/www/html/*
  sudo tar -xzf /tmp/frontend-build.tar.gz -C /var/www/html
  sudo systemctl restart nginx
"
