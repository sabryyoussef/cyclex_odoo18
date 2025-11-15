#!/bin/bash
# Setup virtual environment for Playwright tests

echo "🔧 Setting up Playwright test environment"
echo ""

cd /home/sabry3/edu_demo/custom_addons/cyclex

# Create virtual environment if it doesn't exist
if [ ! -d "venv_test" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_test
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv_test/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements_test.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use:"
echo "  source venv_test/bin/activate"
echo "  ./run_tests.sh"
echo ""
echo "Or run directly:"
echo "  ./venv_test/bin/pytest tests/test_streamlit_ui.py -v"

