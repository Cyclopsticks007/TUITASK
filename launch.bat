@echo off
setlocal

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.10+ and try again.
    pause
    exit /b 1
)

:: Check for virtual environment
if not exist ".venv" (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    python -m pip install -e .
) else (
    call .venv\Scripts\activate.bat
)

:: Run the app
echo Starting TUITASK...
tuitask

if %errorlevel% neq 0 (
    echo TUITASK exited with an error.
    pause
)

endlocal
