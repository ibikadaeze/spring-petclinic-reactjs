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
  
  # Create the missing dist folder explicitly
  sudo mkdir -p /var/www/html/dist
  
  # Extract the bundle assets straight into the dist folder
  sudo tar -xzf /tmp/frontend-build.tar.gz -C /var/www/html/dist
  
  # Move your index.html back up to the absolute root so it can load first
  if [ -f /tmp/index.html ]; then
    sudo mv /tmp/index.html /var/www/html/index.html
  else
    sudo mv /var/www/html/dist/index.html /var/www/html/index.html
  fi

  echo 'Enforcing path traversal and folder permissions...'
  sudo chmod 755 /var /var/www /var/www/html
  sudo chown -R www-data:www-data /var/www/html
  sudo systemctl restart nginx
"
