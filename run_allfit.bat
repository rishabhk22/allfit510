@echo off
setlocal enabledelayedexpansion

:: Colors for output
set "GREEN=[32m"
set "RED=[31m"
set "NC=[0m"

:: Function to print status messages
call :print_status "Checking if setup is required..."

:: Check if setup has been run
if not exist venv\Scripts\activate.bat (
    call :print_status "First-time setup required..."
    call setup.bat
    if %errorlevel% neq 0 (
        echo %RED%Setup failed. Please check the error messages above.%NC%
        exit /b 1
    )
)

:: Activate virtual environment
call :print_status "Activating virtual environment..."
call venv\Scripts\activate.bat

:: Run the application
call :print_status "Starting AllFit application..."
echo %GREEN%The application will be available at: http://localhost:5000%NC%
echo %GREEN%Press Ctrl+C to stop the server%NC%
flask run

exit /b 0

:print_status
echo %GREEN%[*] %~1%NC%
exit /b 0 