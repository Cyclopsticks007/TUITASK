@echo off
setlocal

:: Title for the window
title TUITASK Launcher

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from python.org.
    pause
    exit /b 1
)

:: Check for virtual environment
if not exist ".venv" (
    echo [INFO] Virtual environment not found. Setting up...
    echo [INFO] Creating .venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    
    echo [INFO] Activating .venv...
    call .venv\Scripts\activate.bat
    
    echo [INFO] Upgrading pip...
    python -m pip install --upgrade pip
    
    echo [INFO] Installing tuitask dependencies...
    python -m pip install -e .
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Activating virtual environment...
    call .venv\Scripts\activate.bat
)

:: Run the app
echo [INFO] Starting TUITASK...
echo.
python -m tuitask

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] TUITASK exited with error code %errorlevel%.
    pause
)

endlocal
