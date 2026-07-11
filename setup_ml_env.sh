#!/bin/bash

# Script to set up a Python ML environment on controlplane host
# This script creates a virtual environment and installs ML libraries

set -e

# Navigate to the target directory
cd /root/code/

echo "Step 1: Creating Python virtual environment 'ml-env'..."
python3 -m venv ml-env

echo "Step 2: Activating virtual environment..."
source ml-env/bin/activate

echo "Step 3: Upgrading pip..."
pip install --upgrade pip

echo "Step 4: Installing ML libraries..."
pip install numpy pandas scikit-learn matplotlib

echo "Step 5: Generating requirements.txt..."
pip freeze > requirements.txt

echo "Step 6: Verifying installation..."
echo "Virtual environment path:"
which python
echo ""
echo "Installed packages:"
pip list

echo ""
echo "✓ Setup complete! Virtual environment 'ml-env' is ready at /root/code/ml-env"
echo "✓ requirements.txt saved at /root/code/requirements.txt"
echo ""
echo "To activate the environment in future sessions, run:"
echo "  source /root/code/ml-env/bin/activate"
