#!/bin/bash
# Run Playwright tests for Streamlit app

echo "🧪 Running Playwright UI Tests for CycleX Streamlit App"
echo ""

# Check if Streamlit is running
if ! curl -s http://localhost:8501 > /dev/null 2>&1; then
    echo "❌ Streamlit app is not running on http://localhost:8501"
    echo "   Please start it first:"
    echo "   cd /home/sabry3/edu_demo/custom_addons/cyclex"
    echo "   python3 -m streamlit run streamlit_app.py --server.port 8501"
    exit 1
fi

echo "✅ Streamlit app is running"
echo ""

cd /home/sabry3/edu_demo/custom_addons/cyclex

# Use virtual environment if it exists
if [ -d "venv_test" ]; then
    echo "🔌 Using virtual environment..."
    source venv_test/bin/activate
    PYTEST_CMD="pytest"
else
    echo "⚠️  Virtual environment not found. Using system Python..."
    echo "   Run './setup_test_env.sh' first for better isolation"
    PYTEST_CMD="python3 -m pytest"
fi

# Check if Playwright is installed
if ! python3 -c "import playwright" 2>/dev/null; then
    echo "❌ Playwright not installed!"
    echo "   Run: ./setup_test_env.sh"
    exit 1
fi

echo "🚀 Running tests..."
echo ""

# Run tests
$PYTEST_CMD tests/test_streamlit_ui.py -v "$@"

echo ""
echo "✅ Tests completed!"

