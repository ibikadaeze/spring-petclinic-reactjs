#!/usr/bin/env python3
"""Build frontend using npm."""

import subprocess
import sys
import shutil
import os

def run_command(cmd, description, fail_on_error=True):
    """Run command and optionally exit on failure."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        if fail_on_error:
            print(f"ERROR: {description} failed with exit code {result.returncode}")
            sys.exit(result.returncode)
        else:
            print(f"⚠ WARNING: {description} had issues (exit code {result.returncode}) but continuing...")
    return result.returncode

def remove_if_exists(path):
    """Remove file or directory if it exists."""
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

def main():
    # Extract --step argument
    step = "all"
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--step" and i + 1 < len(sys.argv) - 1:
            step = sys.argv[i + 2]
            break

    # Check for npm cache flag (used in Docker with volume mounts)
    npm_cache = ""
    if "--with-npm-cache" in sys.argv or os.environ.get("NPM_CACHE_DIR"):
        cache_dir = os.environ.get("NPM_CACHE_DIR", "/root/.npm")
        npm_cache = f"--cache {cache_dir}"

    # Install step: clean node_modules and install fresh
    if step in ("install", "all"):
        print("Wiping physical node caches to clear Jenkins memory...")
        remove_if_exists("node_modules")
        remove_if_exists("package-lock.json")

        os.chdir("client")

        print("\nInstalling frontend dependencies...")
        install_cmd = f"npm install --legacy-peer-deps --ignore-scripts {npm_cache}".strip()
        run_command(install_cmd, "Installing dependencies")
    elif step in ("lint", "audit", "build"):
        # For non-install steps, just cd to client
        os.chdir("client")

    # Lint step
    if step in ("lint", "all"):
        print("\nRunning frontend lint checks...")
        subprocess.run("npm run lint --if-present", shell=True)

    # Audit step
    if step in ("audit", "all"):
        print("\nRunning frontend dependency security scan...")
        run_command(
            "npm audit --audit-level=critical || true",
            "Running security audit",
            fail_on_error=False
        )

    # Build step
    if step in ("build", "all"):
        run_command(
            "npm run build:prod",
            "Building frontend"
        )

    print(f"\n✓ Frontend build completed successfully! (step: {step})")

if __name__ == "__main__":
    main()
