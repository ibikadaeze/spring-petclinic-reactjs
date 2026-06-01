#!/usr/bin/env python3
"""Deploy frontend to remote host via SSH."""

import subprocess
import sys
import os
import tarfile

def check_env_var(var_name):
    """Check if environment variable exists."""
    if var_name not in os.environ:
        print(f"ERROR: {var_name} is required")
        sys.exit(1)
    return os.environ[var_name]

def run_command(cmd, description, check=True):
    """Run shell command."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True)
    if check and result.returncode != 0:
        print(f"ERROR: {description} failed")
        sys.exit(result.returncode)
    return result.returncode

def main():
    frontend_host = check_env_var("FRONTEND_HOST")
    frontend_user = check_env_var("FRONTEND_USER")

    # Create tarball from dist directory
    print("Packaging frontend build from client directory...")
    dist_path = "client/public/dist"

    if not os.path.isdir(dist_path):
        print(f"ERROR: {dist_path} directory not found")
        sys.exit(1)

    tar_file = "frontend-build.tar.gz"
    with tarfile.open(tar_file, "w:gz") as tar:
        for item in os.listdir(dist_path):
            item_path = os.path.join(dist_path, item)
            tar.add(item_path, arcname=item)

    print(f"Created {tar_file}")

    # Copy files to remote
    print(f"\nCopying frontend build and index template to {frontend_host}...")
    run_command(
        f'scp {tar_file} {frontend_user}@{frontend_host}:/tmp/{tar_file}',
        "Copying tarball"
    )
    run_command(
        f'scp client/public/index.html {frontend_user}@{frontend_host}:/tmp/index.html',
        "Copying index.html"
    )

    # Deploy to web root
    deploy_cmd = f"""ssh {frontend_user}@{frontend_host} "
      # 1. Clean out the web root entirely
      sudo rm -rf /var/www/html/*

      # 2. Recreate the absolute web root and an explicit matching dist subfolder
      sudo mkdir -p /var/www/html/dist

      # 3. Extract the assets (bundle.js, styles.css, images) straight into /dist
      sudo tar -xzf /tmp/{tar_file} -C /var/www/html/dist

      # 4. Move index.html up to the absolute root so it loads first
      sudo mv /tmp/index.html /var/www/html/index.html

      # 5. Clean up temporary files
      sudo rm -f /tmp/{tar_file}

      echo 'Enforcing precise path traversal and folder permissions...'
      sudo chmod 755 /var /var/www /var/www/html
      sudo chown -R www-data:www-data /var/www/html
      sudo find /var/www/html -type d -exec chmod 755 {{}} +
      sudo find /var/www/html -type f -exec chmod 644 {{}} +

      sudo systemctl restart nginx
    " """

    print("Deploying frontend build to Nginx web root...")
    run_command(deploy_cmd, "Deploying to remote host")

    # Cleanup
    os.remove(tar_file)
    print(f"\nCleaned up {tar_file}")

    print("\n✓ Frontend deployment completed successfully!")

if __name__ == "__main__":
    main()
