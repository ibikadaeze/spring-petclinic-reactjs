#!/usr/bin/env python3
"""Smoke test frontend availability."""

import subprocess
import sys
import time
import os

def check_env_var(var_name):
    """Check if environment variable exists."""
    if var_name not in os.environ:
        print(f"ERROR: {var_name} is required")
        sys.exit(1)
    return os.environ[var_name]

def main():
    frontend_host = check_env_var("FRONTEND_HOST")
    frontend_url = f"http://{frontend_host}/"

    print("Waiting for frontend to settle...")
    time.sleep(5)

    print(f"\nChecking {frontend_url}...")
    result = subprocess.run(f'curl -f "{frontend_url}"', shell=True)

    if result.returncode != 0:
        print("\nERROR: Frontend smoke test failed")
        sys.exit(1)

    print("\n✓ Frontend smoke test passed!")

if __name__ == "__main__":
    main()
