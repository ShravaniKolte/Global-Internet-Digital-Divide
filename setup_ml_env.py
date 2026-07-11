#!/usr/bin/env python3

"""
Setup script for ML environment on controlplane host.
This script creates a virtual environment and installs required ML libraries.
Run this script with: python3 setup_ml_env.py
"""

import os
import subprocess
import sys

def run_command(cmd, description):
    """Execute a shell command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=False, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description} failed with exit code {e.returncode}")
        return False

def main():
    """Main setup function."""
    
    target_dir = "/root/code"
    venv_name = "ml-env"
    venv_path = os.path.join(target_dir, venv_name)
    
    print("=" * 60)
    print("ML Environment Setup Script")
    print("=" * 60)
    
    # Step 1: Check if directory exists
    if not os.path.exists(target_dir):
        print(f"✗ Error: Target directory {target_dir} does not exist")
        sys.exit(1)
    
    os.chdir(target_dir)
    print(f"\n✓ Working directory: {os.getcwd()}")
    
    # Step 2: Create virtual environment
    if not run_command(f"python3 -m venv {venv_name}", 
                       "Step 1: Creating virtual environment 'ml-env'"):
        sys.exit(1)
    
    # Step 3: Activate and install packages
    activate_cmd = f"source {venv_path}/bin/activate"
    
    # Upgrade pip
    if not run_command(f"{activate_cmd} && pip install --upgrade pip",
                       "Step 2: Upgrading pip"):
        sys.exit(1)
    
    # Install ML libraries
    ml_packages = ["numpy", "pandas", "scikit-learn", "matplotlib"]
    packages_str = " ".join(ml_packages)
    
    if not run_command(f"{activate_cmd} && pip install {packages_str}",
                       "Step 3: Installing ML libraries"):
        sys.exit(1)
    
    # Step 4: Generate requirements.txt
    requirements_path = os.path.join(target_dir, "requirements.txt")
    if not run_command(f"{activate_cmd} && pip freeze > {requirements_path}",
                       "Step 4: Generating requirements.txt"):
        sys.exit(1)
    
    # Step 5: Verify installation
    print("\n" + "=" * 60)
    print("Verification")
    print("=" * 60)
    run_command(f"{activate_cmd} && pip list", "Installed packages")
    
    if os.path.exists(requirements_path):
        print(f"\n✓ requirements.txt contents:")
        with open(requirements_path, 'r') as f:
            print(f.read())
    
    print("\n" + "=" * 60)
    print("✓ Setup Complete!")
    print("=" * 60)
    print(f"\nVirtual environment location: {venv_path}")
    print(f"Requirements file: {requirements_path}")
    print(f"\nTo activate the environment, run:")
    print(f"  source {venv_path}/bin/activate")

if __name__ == "__main__":
    main()
