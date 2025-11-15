# 🚀 Quick Start - Playwright Testing

## Install & Run (One Command)

```bash
cd /home/sabry3/edu_demo/custom_addons/cyclex

# Install dependencies
pip3 install -r requirements_test.txt
playwright install chromium

# Run all tests
./run_tests.sh
```

## Quick Test

```bash
# Run one test
pytest tests/test_streamlit_ui.py::TestStreamlitUI::test_splash_screen_loads -v

# Run with visible browser
pytest tests/test_streamlit_ui.py -v --headed

# Run all tests
pytest tests/test_streamlit_ui.py -v
```

## Prerequisites

1. ✅ Streamlit app running on http://localhost:8501
2. ✅ Python 3.8+
3. ✅ Playwright installed

## Test Coverage

- ✅ Splash screen
- ✅ Login (demo & form)
- ✅ Navigation tabs
- ✅ All main screens
- ✅ Logout

See `PLAYWRIGHT_TESTING_GUIDE.md` for full details.

