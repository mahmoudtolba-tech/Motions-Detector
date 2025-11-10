@echo off
REM Advanced Motion Detector Run Script for Windows
REM This script activates the virtual environment and runs the application

echo ================================================================
echo.
echo   █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗
echo  ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝
echo  ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║      █████╗
echo  ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║      ██╔══╝
echo  ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗ ███████╗
echo  ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
echo.
echo          MOTION DETECTOR PRO v2.0 for Windows
echo.
echo ================================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Check if dependencies are installed
echo [2/3] Checking dependencies...
python -c "import cv2, customtkinter, pandas, matplotlib" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Some dependencies are missing!
    echo Please run setup.bat to install dependencies
    pause
    exit /b 1
)
echo [OK] All dependencies found
echo.

REM Run the application
echo [3/3] Starting Motion Detector...
echo.
echo ================================================================
echo   Motion Detector is starting...
echo   Press Ctrl+C to stop or close the window
echo ================================================================
echo.

python motion_detector_gui.py

REM Deactivate on exit
call venv\Scripts\deactivate.bat >nul 2>&1

pause
