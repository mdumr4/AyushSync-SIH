@echo off
:: This script assumes it is being run from the project root directory.

echo Activating virtual environment...

:: Check if the virtual environment activation script exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo Please ensure the .venv directory exists in this folder.
    pause
    exit /b
)

:: Activate the virtual environment
call .venv\Scripts\activate.bat

echo.
echo Starting Backend API Server (Uvicorn) in a new window...
:: Use "python -m" to be explicit about using the venv's python
start "Backend API" cmd /k python -m uvicorn prototype.main:app --host 0.0.0.0 --port 8000

echo.
echo Starting Frontend UI Server (Streamlit) in a new window...
timeout /t 5 >nul

:: Use "python -m" for streamlit as well
start "Frontend UI" cmd /k python -m streamlit run prototype/app.py

echo.
echo Two new windows have been opened. Please check the Streamlit window for the URL.