@echo off
REM ====================================
REM Start Script for CommerceBot Backend
REM Last Modified: 2026-03-30 19:00
REM ====================================

echo.
echo ====================================
echo CommerceBot - Starting Backend Service
echo ====================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found
    echo Please run setup_env.bat first to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check .env file
echo [2/3] Checking environment configuration...
if not exist .env (
    echo Copying environment config template...
    copy .env.example .env
    echo.
    echo WARNING: Please edit .env file to configure database password
    echo Run this script again after configuration
    pause
    exit /b 0
)

REM Start backend service
echo [3/3] Starting backend service...
echo.
echo ====================================
echo Backend service starting...
echo API URL: http://localhost:8765
echo API Docs: http://localhost:8765/docs
echo Press Ctrl+C to stop service
echo ====================================
echo.

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8765 --reload

pause
