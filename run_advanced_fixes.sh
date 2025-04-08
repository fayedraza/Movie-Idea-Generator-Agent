#!/bin/bash
# Script to run advanced fixes and then check the pylint score

set -e  # Exit on error

echo "===== STEP 1: Running advanced fixes ====="
# Make sure the script is executable
chmod +x advanced_fixes.py
# Run the advanced fixes script
python advanced_fixes.py

echo "===== STEP 2: Running format and check script ====="
# Make sure the script is executable
chmod +x format_and_check.sh
# Run the format and check script
./format_and_check.sh

echo "All fixes and checks completed!" 