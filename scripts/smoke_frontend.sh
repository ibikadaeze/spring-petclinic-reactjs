#!/usr/bin/env bash
set -euo pipefail

: "${FRONTEND_HOST:?FRONTEND_HOST is required}"

FRONTEND_URL="http://${FRONTEND_HOST}/"

echo "Waiting for frontend to settle..."
sleep 5

echo "Checking ${FRONTEND_URL}..."
curl -f "${FRONTEND_URL}"
