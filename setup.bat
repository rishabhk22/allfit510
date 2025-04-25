@echo off
setlocal enabledelayedexpansion

:: Colors for output
set "GREEN=[32m"
set "RED=[31m"
set "NC=[0m"

:: Function to print status messages
call :print_status "Checking Python installation..."
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%Python is not installed. Please install Python and try again.%NC%
    exit /b 1
)

:: Create and activate virtual environment
call :print_status "Creating virtual environment..."
python -m venv venv
call venv\Scripts\activate.bat

:: Upgrade pip
call :print_status "Upgrading pip..."
python -m pip install --upgrade pip

:: Install requirements
call :print_status "Installing requirements..."
pip install -r requirements.txt

:: Create instance directory
call :print_status "Creating instance directory..."
if not exist instance mkdir instance

:: Create .env file if it doesn't exist
if not exist .env (
    call :print_status "Creating .env file..."
    copy .env.example .env
    :: Generate a random secret key
    for /f "delims=" %%a in ('python -c "import secrets; print(secrets.token_hex(32))"') do set "SECRET_KEY=%%a"
    powershell -Command "(Get-Content .env) -replace 'your-secret-key-here', '%SECRET_KEY%' | Set-Content .env"
)

:: Initialize database
call :print_status "Initializing database..."
flask db init
flask db migrate
flask db upgrade

call :print_status "Setup completed successfully!"
echo.
echo To run the application:
echo 1. Activate the virtual environment: %GREEN%venv\Scripts\activate%NC%
echo 2. Run the application: %GREEN%flask run%NC%
echo.
echo The application will be available at: %GREEN%http://localhost:5000%NC%

exit /b 0

:print_status
echo %GREEN%[*] %~1%NC%
exit /b 0 