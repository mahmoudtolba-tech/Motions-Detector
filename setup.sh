#!/bin/bash

# Advanced Motion Detector Setup Script
# This script sets up the virtual environment and installs all dependencies

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════╗"
echo "║    Advanced Motion Detector - Setup Script              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
echo -e "${BLUE}[1/6]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
echo ""

# Check Python version (must be 3.8+)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}Error: Python 3.8 or higher is required!${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}[2/6]${NC} Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠${NC}  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
echo -e "${GREEN}✓${NC} Virtual environment created"
echo ""

# Activate virtual environment
echo -e "${BLUE}[3/6]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Upgrade pip
echo -e "${BLUE}[4/6]${NC} Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip upgraded"
echo ""

# Install dependencies
echo -e "${BLUE}[5/6]${NC} Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} All dependencies installed successfully"
else
    echo -e "${RED}✗${NC} Error installing dependencies"
    exit 1
fi
echo ""

# Create necessary directories
echo -e "${BLUE}[6/6]${NC} Creating project directories..."
mkdir -p recordings snapshots exports
echo -e "${GREEN}✓${NC} Directories created:"
echo "  - recordings/ (for video recordings)"
echo "  - snapshots/  (for camera snapshots)"
echo "  - exports/    (for data exports)"
echo ""

# Create default config if doesn't exist
if [ ! -f "config.json" ]; then
    echo -e "${BLUE}Creating default configuration...${NC}"
    cat > config.json << 'EOF'
{
    "camera": {
        "index": 0,
        "width": 640,
        "height": 480,
        "fps": 30
    },
    "detection": {
        "algorithm": "mog2",
        "sensitivity": 50,
        "min_area": 5000,
        "bg_threshold": 16,
        "blur_kernel": 21,
        "dilation_iterations": 2
    },
    "recording": {
        "enabled": true,
        "codec": "mp4v",
        "output_dir": "recordings"
    },
    "notifications": {
        "enabled": false,
        "cooldown": 60,
        "desktop_enabled": true,
        "email_enabled": false
    }
}
EOF
    echo -e "${GREEN}✓${NC} Default configuration created"
fi
echo ""

# Setup complete
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! 🎉                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}To run the motion detector:${NC}"
echo "  ./run.sh"
echo ""
echo -e "${YELLOW}Note:${NC} Make sure you have a webcam connected!"
echo ""
echo -e "${BLUE}For more information, see README.md${NC}"
