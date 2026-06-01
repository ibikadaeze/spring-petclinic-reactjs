#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_HOST:?FRONTEND_HOST is required}"
: "${FRONTEND_USER:?FRONTEND_USER is required}"

echo "Packaging frontend build..."
tar -czf frontend-build.tar.gz -C client/public/dist .

echo "Copying frontend build to ${FRONTEND_HOST}..."
scp frontend-build.tar.gz "${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/frontend-build.tar.gz"

# STEP 1: Copy your parent index.html framework template over if it sits outside dist folder
echo "Copying root HTML templates..."
scp client/public/index.html "${FRONTEND_USER}@${FRONTEND_HOST}:/tmp/index.html" || true

echo "Deploying frontend build to Nginx..."
ssh "${FRONTEND_USER}@${FRONTEND_HOST}" "
  sudo rm -rf /var/www/html/*
  sudo tar -xzf /tmp/frontend-build.tar.gz -C /var/www/html
  
  # Copy index.html to the web root if it was extracted to /tmp
  if [ -f /tmp/index.html ]; then
    sudo mv /tmp/index.html /var/www/html/index.html
  fi

  echo 'Enforcing path traversal and folder permissions...'
  # Fix parent directory visibility issues
  sudo chmod 755 /var /var/www /var/www/html
  
  # Ensure all contents inside the web root are readable
  sudo chown -R www-data:www-data /var/www/html
  sudo find /var/www/html -type d -exec chmod 755 {} +
  sudo find /var/www/html -type f -exec chmod 644 {} +
  
  sudo systemctl restart nginx
"
