# ML Environment Setup for xFusionCorp Industries

This solution provides scripts to set up a standardized Python machine learning environment on the `controlplane` host.

## Requirements

- Python 3.6 or higher
- Access to `/root/code/` directory on the controlplane host
- Internet access to download packages

## End State

After running this setup, you will have:

✓ A Python virtual environment named `ml-env` at `/root/code/ml-env/`
✓ ML libraries installed: `numpy`, `pandas`, `scikit-learn`, `matplotlib`
✓ A `requirements.txt` file at `/root/code/requirements.txt` capturing all installed packages

## Setup Instructions

### Option 1: Using Bash Script (Recommended)

1. Copy `setup_ml_env.sh` to the controlplane host at `/root/code/`
2. Make it executable and run:

```bash
cd /root/code
chmod +x setup_ml_env.sh
./setup_ml_env.sh
```

### Option 2: Using Python Script

1. Copy `setup_ml_env.py` to the controlplane host at `/root/code/`
2. Run the script:

```bash
cd /root/code
python3 setup_ml_env.py
```

### Option 3: Manual Setup

Run these commands directly on the controlplane host:

```bash
# Navigate to working directory
cd /root/code

# Create virtual environment
python3 -m venv ml-env

# Activate virtual environment
source ml-env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install ML libraries
pip install numpy pandas scikit-learn matplotlib

# Generate requirements.txt
pip freeze > requirements.txt
```

## Verification

To verify the setup was successful:

```bash
# Activate the environment
source /root/code/ml-env/bin/activate

# Check installed packages
pip list

# Display requirements.txt
cat /root/code/requirements.txt
```

## Usage

To use the ML environment in future sessions:

```bash
# Activate the environment
source /root/code/ml-env/bin/activate

# Deactivate the environment (when done)
deactivate
```

## Installed Packages

- **numpy**: Numerical computing library
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning algorithms
- **matplotlib**: Data visualization

## Troubleshooting

### Issue: Python3 not found
**Solution**: Use `python` instead of `python3`, or install Python 3.

### Issue: Permission denied
**Solution**: Ensure you have write permissions to `/root/code/` directory.

### Issue: venv module not found
**Solution**: Install venv package - `apt-get install python3-venv` (Ubuntu/Debian) or `yum install python3-venv` (RHEL/CentOS)

## Files Included

- `setup_ml_env.sh` - Bash script for automated setup
- `setup_ml_env.py` - Python script for automated setup
- `SETUP_SOLUTION.md` - This documentation file

## Support

For issues or questions about the ML environment setup, refer to the requirements.txt file or run the setup script with detailed output.
