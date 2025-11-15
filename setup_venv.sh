#!/bin/bash

# CycleX Virtual Environment Setup Script for Odoo 18
# This script creates and configures a Python virtual environment

set -e  # Exit on error

echo "=========================================="
echo "CycleX - Odoo 18 Virtual Environment Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python3.12 --version

# Create virtual environment
echo -e "${BLUE}Creating virtual environment 'venv'...${NC}"
python3.12 -m venv venv

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip setuptools wheel

# Install Python development headers (needed for some packages)
echo -e "${YELLOW}Note: Make sure you have python3-dev installed on your system${NC}"
echo -e "${YELLOW}If not, run: sudo apt-get install python3-dev libpq-dev libldap2-dev libsasl2-dev${NC}"
echo ""

# Install requirements
echo -e "${BLUE}Installing Python dependencies from requirements.txt...${NC}"
pip install -r requirements.txt

echo ""
echo -e "${GREEN}=========================================="
echo -e "Virtual environment setup complete! ✓"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}To activate the virtual environment, run:${NC}"
echo -e "  source venv/bin/activate"
echo ""
echo -e "${YELLOW}To deactivate, run:${NC}"
echo -e "  deactivate"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Clone Odoo 18 repository (if not already done)"
echo -e "  2. Add the CycleX module to your Odoo addons path"
echo -e "  3. Start Odoo with: python odoo-bin -c /path/to/config.conf"
echo ""

