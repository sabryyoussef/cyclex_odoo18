#!/bin/bash
# Install Playwright for testing

echo "📦 Installing Playwright for UI Testing"
echo ""

# Install Python packages
echo "1. Installing Python packages..."
python3 -m pip install --user pytest playwright pytest-playwright pytest-asyncio

# Install Playwright browsers
echo ""
echo "2. Installing Playwright browsers..."
python3 -m playwright install chromium

echo ""
echo "✅ Installation complete!"
echo ""
echo "To run tests:"
echo "  ./run_tests.sh"
echo "  or"
echo "  python3 -m pytest tests/test_streamlit_ui.py -v"

