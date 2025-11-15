# 🎭 Playwright Setup & Usage

## Quick Setup

### Option 1: Virtual Environment (Recommended)
```bash
cd /home/sabry3/edu_demo/custom_addons/cyclex
./setup_test_env.sh
```

This will:
- Create a virtual environment (`venv_test`)
- Install all dependencies
- Install Playwright browsers

### Option 2: Manual Installation
```bash
# Create venv
python3 -m venv venv_test
source venv_test/bin/activate

# Install
pip install -r requirements_test.txt
playwright install chromium
```

---

## Running Tests

### Quick Run
```bash
./run_tests.sh
```

### With Virtual Environment
```bash
source venv_test/bin/activate
pytest tests/test_streamlit_ui.py -v
```

### Specific Tests
```bash
# One test
pytest tests/test_streamlit_ui.py::TestStreamlitUI::test_splash_screen_loads -v

# With visible browser
pytest tests/test_streamlit_ui.py -v --headed

# All tests
pytest tests/test_streamlit_ui.py -v
```

---

## Prerequisites

1. ✅ Streamlit app running: `http://localhost:8501`
2. ✅ Python 3.8+
3. ✅ Virtual environment (optional but recommended)

---

## Test Files Created

- ✅ `tests/test_streamlit_ui.py` - Main test suite
- ✅ `tests/conftest.py` - Pytest configuration
- ✅ `pytest.ini` - Pytest settings
- ✅ `run_tests.sh` - Test runner
- ✅ `setup_test_env.sh` - Environment setup

---

## Troubleshooting

### "No module named playwright"
```bash
./setup_test_env.sh
source venv_test/bin/activate
```

### "Streamlit not running"
```bash
# Start Streamlit first
python3 -m streamlit run streamlit_app.py --server.port 8501
```

### Permission errors
```bash
chmod +x setup_test_env.sh run_tests.sh
```

---

**Ready to test!** 🚀

