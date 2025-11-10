#!/bin/bash

# Advanced Motion Detector Run Script
# This script activates the virtual environment and runs the application

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ASCII Art Banner
cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗ ██████╗  ║
║  ██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║██╔════╝  ║
║  ███████║██║  ██║██║   ██║███████║██╔██╗ ██║██║       ║
║  ██╔══██║██║  ██║╚██╗ ██╔╝██╔══██║██║╚██╗██║██║       ║
║  ██║  ██║██████╔╝ ╚████╔╝ ██║  ██║██║ ╚████║╚██████╗  ║
║  ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ║
║                                                          ║
║          MOTION DETECTOR PRO v2.0                       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF

echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found!${NC}"
    echo -e "${YELLOW}Please run setup.sh first:${NC}"
    echo "  chmod +x setup.sh"
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}[1/3]${NC} Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"
echo ""

# Check if dependencies are installed
echo -e "${BLUE}[2/3]${NC} Checking dependencies..."
python3 -c "import cv2, customtkinter, pandas, matplotlib" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}✗${NC} Some dependencies are missing!"
    echo -e "${YELLOW}Please run setup.sh to install dependencies${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} All dependencies found"
echo ""

# Check for camera
echo -e "${BLUE}[3/3]${NC} Starting Motion Detector..."
echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  Motion Detector is starting...       ║${NC}"
echo -e "${GREEN}║  Press Ctrl+C to stop                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Run the application
python3 motion_detector_gui.py

# Deactivate virtual environment on exit
deactivate 2>/dev/null || true
