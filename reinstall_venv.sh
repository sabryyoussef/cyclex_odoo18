#!/bin/bash

# CycleX - Reinstall Virtual Environment with Python 3.12

set -e  # Exit on error

echo "=========================================="
echo "CycleX - Reinstalling Virtual Environment"
echo "Using Python 3.12"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python 3.12 is installed
echo -e "${BLUE}Checking for Python 3.12...${NC}"
if ! command -v python3.12 &> /dev/null; then
    echo -e "${RED}Error: Python 3.12 is not installed!${NC}"
    echo -e "${YELLOW}Install it with: sudo apt-get install python3.12 python3.12-venv python3.12-dev${NC}"
    exit 1
fi

python3.12 --version
echo ""

# Remove old venv if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Removing existing virtual environment...${NC}"
    rm -rf venv
    echo -e "${GREEN}✓ Old venv removed${NC}"
    echo ""
fi

# Create new virtual environment with Python 3.12
echo -e "${BLUE}Creating new virtual environment with Python 3.12...${NC}"
python3.12 -m venv venv

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip, setuptools, and wheel...${NC}"
pip install --upgrade pip setuptools wheel

# Install requirements
echo -e "${BLUE}Installing Python dependencies from requirements.txt...${NC}"
pip install -r requirements.txt

echo ""
echo -e "${GREEN}=========================================="
echo -e "✓ Virtual environment reinstalled successfully!"
echo -e "✓ Python version: $(python --version)"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "  source venv/bin/activate"
echo ""
echo -e "${YELLOW}Verify installation:${NC}"
echo -e "  python --version"
echo -e "  pip list"
echo ""

