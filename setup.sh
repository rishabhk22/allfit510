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

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Create and activate virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing requirements..."
pip install -r requirements.txt

# Create instance directory
print_status "Creating instance directory..."
mkdir -p instance

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file..."
    cp .env.example .env
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    sed -i '' "s/your-secret-key-here/$SECRET_KEY/" .env
fi

# Initialize database
print_status "Initializing database..."
flask db init
flask db migrate
flask db upgrade

print_status "Setup completed successfully!"
echo -e "\nTo run the application:"
echo -e "1. Activate the virtual environment: ${GREEN}source venv/bin/activate${NC}"
echo -e "2. Run the application: ${GREEN}flask run${NC}"
echo -e "\nThe application will be available at: ${GREEN}http://localhost:5000${NC}" 