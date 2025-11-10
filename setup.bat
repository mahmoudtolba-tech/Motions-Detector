@echo off
REM Advanced Motion Detector Setup Script for Windows
REM This script sets up the virtual environment and installs all dependencies

echo ================================================================
echo    Advanced Motion Detector - Setup Script for Windows
echo ================================================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher and add it to PATH.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment!
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded
echo.

REM Install dependencies
echo [5/6] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    pause
    exit /b 1
)
echo [OK] All dependencies installed successfully
echo.

REM Create necessary directories
echo [6/6] Creating project directories...
if not exist recordings mkdir recordings
if not exist snapshots mkdir snapshots
if not exist exports mkdir exports
echo [OK] Directories created:
echo   - recordings\ (for video recordings)
echo   - snapshots\  (for camera snapshots)
echo   - exports\    (for data exports)
echo.

REM Create default config if doesn't exist
if not exist config.json (
    echo Creating default configuration...
    (
        echo {
        echo     "camera": {
        echo         "index": 0,
        echo         "width": 640,
        echo         "height": 480,
        echo         "fps": 30
        echo     },
        echo     "detection": {
        echo         "algorithm": "mog2",
        echo         "sensitivity": 50,
        echo         "min_area": 5000,
        echo         "bg_threshold": 16,
        echo         "blur_kernel": 21,
        echo         "dilation_iterations": 2
        echo     },
        echo     "recording": {
        echo         "enabled": true,
        echo         "codec": "mp4v",
        echo         "output_dir": "recordings"
        echo     },
        echo     "notifications": {
        echo         "enabled": false,
        echo         "cooldown": 60,
        echo         "desktop_enabled": true,
        echo         "email_enabled": false
        echo     }
        echo }
    ) > config.json
    echo [OK] Default configuration created
)
echo.

echo ================================================================
echo               Setup Complete!
echo ================================================================
echo.
echo To run the motion detector:
echo   run.bat
echo.
echo Note: Make sure you have a webcam connected!
echo.
echo For more information, see README.md
echo.
pause
