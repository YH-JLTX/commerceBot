@echo off
REM ====================================
REM Environment Setup Script for CommerceBot
REM Last Modified: 2026-03-30 19:00
REM ====================================

echo.
echo ====================================
echo CommerceBot - Environment Setup
echo ====================================
echo.

REM Check Python version
echo [1/5] Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.10+
    pause
    exit /b 1
)

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping creation
) else (
    python -m venv venv
    echo Virtual environment created successfully
)

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [4/5] Upgrading pip to latest version...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

REM Install dependencies
echo [5/5] Installing project dependencies...
echo Using Tsinghua mirror for faster download...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo To activate virtual environment:
echo   venv\Scripts\activate.bat
echo.
echo To deactivate virtual environment:
echo   deactivate
echo.
echo Make sure virtual environment is activated for development
echo.
pause
