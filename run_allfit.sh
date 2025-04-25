#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[*] $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}[!] $1${NC}"
}

# Check if setup has been run
if [ ! -d "venv" ] || [ ! -f ".env" ]; then
    print_status "First-time setup required..."
    ./setup.sh
    if [ $? -ne 0 ]; then
        print_error "Setup failed. Please check the error messages above."
        exit 1
    fi
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Run the application
print_status "Starting AllFit application..."
print_status "The application will be available at: http://localhost:5001"
print_status "Press Ctrl+C to stop the server"
flask run -p 5001 