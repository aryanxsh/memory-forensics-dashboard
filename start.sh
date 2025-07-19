#!/bin/bash

echo "========================================"
echo "   Memory Forensics Dashboard"
echo "========================================"
echo ""
echo "Starting the web dashboard..."
echo ""
echo "Access the dashboard at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found"
    exit 1
fi

# Install requirements if needed
echo "Checking dependencies..."
pip3 install -r requirements.txt

# Start the application
python3 app.py 