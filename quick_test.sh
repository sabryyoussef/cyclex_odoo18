#!/bin/bash
# Quick test runner

echo "🧪 Quick Playwright Test"
echo ""

# Check Streamlit
if curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "✅ Streamlit running"
else
    echo "❌ Start Streamlit first!"
    exit 1
fi

# Install if needed
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "📦 Installing Playwright..."
    pip3 install -q pytest playwright pytest-playwright
    playwright install chromium
fi

# Run one quick test
echo "🚀 Running test..."
pytest tests/test_streamlit_ui.py::TestStreamlitUI::test_splash_screen_loads -v --headed
