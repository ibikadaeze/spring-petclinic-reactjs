#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_HOST:?FRONTEND_HOST is required}"
: "${FRONTEND_USER:?FRONTEND_USER is required}"

echo "Packaging frontend build from client directory..."
# This cleanly packages everything inside the true output folder
tar -czf frontend-build.tar.gz -C client/public/dist .

echo "Copying frontend build and index template to ${FRONTEND_HOST}..."
scp frontend-build.tar.gz "${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/frontend-build.tar.gz"
scp client/public/index.html "${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/index.html"

echo "Deploying frontend build to Nginx web root..."
ssh "${FRONTEND_USER}@${FRONTEND_HOST}" "
  # 1. Clean out the web root entirely
  sudo rm -rf /var/www/html/*
  
  # 2. Recreate the absolute web root and an explicit matching dist subfolder
  sudo mkdir -p /var/www/html/dist
  
  # 3. Extract the assets (bundle.js, styles.css, images) straight into /dist
  sudo tar -xzf /tmp/frontend-build.tar.gz -C /var/www/html/dist
  
  # 4. Move index.html up to the absolute root so it loads first
  sudo mv /tmp/index.html /var/www/html/index.html
  
  # 5. Clean up temporary files
  sudo rm -f /tmp/frontend-build.tar.gz

  echo 'Enforcing precise path traversal and folder permissions...'
  sudo chmod 755 /var /var/www /var/www/html
  sudo chown -R www-data:www-data /var/www/html
  sudo find /var/www/html -type d -exec chmod 755 {} +
  sudo find /var/www/html -type f -exec chmod 644 {} +
  
  sudo systemctl restart nginx
"
