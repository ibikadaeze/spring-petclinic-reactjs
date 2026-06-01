#!/usr/bin/env python3
"""Build frontend using npm."""

import subprocess
import sys
import shutil
import os

def run_command(cmd, description):
    """Run command and exit on failure."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: {description} failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def remove_if_exists(path):
    """Remove file or directory if it exists."""
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def main():
    print("Wiping physical node caches to clear Jenkins memory...")
    remove_if_exists("node_modules")
    remove_if_exists("package-lock.json")

    os.chdir("client")

    print("\nInstalling frontend dependencies...")
    run_command(
        "npm install --legacy-peer-deps --ignore-scripts",
        "Installing dependencies"
    )

    print("\nRunning frontend dependency security scan...")
    subprocess.run("npm audit --audit-level=critical || true", shell=True)

    print("\nRunning frontend lint checks...")
    subprocess.run("npm run lint --if-present", shell=True)

    run_command(
        "npm run build:prod",
        "Building frontend"
    )

    print("\n✓ Frontend build completed successfully!")

if __name__ == "__main__":
    main()
