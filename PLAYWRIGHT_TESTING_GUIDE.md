# 🎭 Playwright UI Testing Guide

## Overview
This guide explains how to run Playwright tests for the CycleX Streamlit application.

---

## 📦 Installation

### 1. Install Dependencies
```bash
cd /home/sabry3/edu_demo/custom_addons/cyclex
pip3 install -r requirements_test.txt
```

### 2. Install Playwright Browsers
```bash
playwright install chromium
```

### 3. Verify Installation
```bash
python3 -c "import playwright; print('Playwright installed')"
```

---

## 🚀 Running Tests

### Quick Start
```bash
cd /home/sabry3/edu_demo/custom_addons/cyclex
./run_tests.sh
```

### Run Specific Tests
```bash
# Run all tests
pytest tests/test_streamlit_ui.py -v

# Run specific test
pytest tests/test_streamlit_ui.py::TestStreamlitUI::test_demo_login_customer -v

# Run with browser visible (headed mode)
pytest tests/test_streamlit_ui.py -v --headed

# Run in headless mode (default)
pytest tests/test_streamlit_ui.py -v --headless
```

### Run Tests with Options
```bash
# Run with screenshots on failure
pytest tests/test_streamlit_ui.py -v --screenshot=only-on-failure

# Run with video recording
pytest tests/test_streamlit_ui.py -v --video=on

# Run specific marker
pytest tests/test_streamlit_ui.py -v -m ui
```

---

## 📋 Test Coverage

### Current Tests

#### Authentication Tests
- ✅ `test_splash_screen_loads` - Splash screen displays
- ✅ `test_navigate_to_login` - Navigation to login
- ✅ `test_demo_login_customer` - Quick customer login
- ✅ `test_demo_login_collector` - Quick collector login
- ✅ `test_form_login` - Form-based login
- ✅ `test_logout` - Logout functionality
- ✅ `test_signup_navigation` - Signup screen navigation

#### Navigation Tests
- ✅ `test_navigation_tabs_customer` - Tab navigation
- ✅ `test_categories_screen` - Categories screen
- ✅ `test_create_order_screen` - Create order screen
- ✅ `test_my_orders_screen` - Orders screen
- ✅ `test_profile_screen` - Profile screen
- ✅ `test_wallet_access` - Wallet access

#### API Tests (Skipped by default)
- ⏭️ `test_real_api_login` - Real API login (requires USE_DEMO_DATA = False)

---

## 🔧 Configuration

### Test Settings
Edit `tests/test_streamlit_ui.py`:
```python
STREAMLIT_URL = "http://localhost:8501"  # Change if needed
TIMEOUT = 10000  # 10 seconds timeout
```

### Browser Settings
Edit `tests/conftest.py`:
```python
browser = playwright.chromium.launch(
    headless=False,  # Set to True for CI/headless mode
    slow_mo=1000     # Add delay between actions (optional)
)
```

---

## 📊 Test Reports

### Generate HTML Report
```bash
pytest tests/test_streamlit_ui.py -v --html=report.html --self-contained-html
```

### Generate JUnit XML (for CI)
```bash
pytest tests/test_streamlit_ui.py -v --junitxml=results.xml
```

---

## 🐛 Debugging Tests

### Run with Debug Output
```bash
pytest tests/test_streamlit_ui.py -v -s --headed
```

### Pause on Failure
```bash
pytest tests/test_streamlit_ui.py -v --headed --pdb
```

### Take Screenshot on Failure
```bash
pytest tests/test_streamlit_ui.py -v --screenshot=only-on-failure
```

### View Test Execution
```bash
# Run with visible browser
pytest tests/test_streamlit_ui.py -v --headed

# Run with slow motion
# Edit conftest.py: slow_mo=1000
```

---

## 📝 Writing New Tests

### Test Template
```python
def test_your_feature(self, page: Page):
    """Test description"""
    # Navigate
    page.goto(STREAMLIT_URL)
    time.sleep(1)
    
    # Perform actions
    page.click("button:has-text('Button Text')")
    time.sleep(1)
    
    # Assertions
    expect(page.locator("text=Expected Text")).to_be_visible()
```

### Best Practices
1. Use `time.sleep()` for Streamlit rendering delays
2. Use `expect()` for assertions
3. Use descriptive test names
4. Group related tests in classes
5. Use fixtures for setup/teardown

---

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: UI Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements_test.txt
      - run: playwright install chromium
      - run: pytest tests/test_streamlit_ui.py -v --headless
```

---

## ⚠️ Troubleshooting

### Issue: Tests fail with timeout
**Solution:**
- Increase `TIMEOUT` in test file
- Check if Streamlit is running
- Verify app loads correctly

### Issue: Elements not found
**Solution:**
- Check Streamlit app is on correct screen
- Add more `time.sleep()` delays
- Use `page.wait_for_selector()` instead

### Issue: Browser not launching
**Solution:**
- Run `playwright install chromium`
- Check browser path
- Try different browser: `playwright.firefox.launch()`

### Issue: Tests are flaky
**Solution:**
- Increase wait times
- Use `page.wait_for_load_state()`
- Add explicit waits for elements

---

## 📈 Test Metrics

### Run with Coverage
```bash
pytest tests/test_streamlit_ui.py -v --cov=streamlit_app --cov-report=html
```

### Performance Testing
```bash
# Add timing to tests
import time
start = time.time()
# ... test actions ...
duration = time.time() - start
assert duration < 5.0  # Should complete in 5 seconds
```

---

## 🔗 Related Files

- `tests/test_streamlit_ui.py` - Main test file
- `tests/conftest.py` - Pytest configuration
- `pytest.ini` - Pytest settings
- `run_tests.sh` - Test runner script
- `requirements_test.txt` - Test dependencies

---

## 📚 Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Streamlit Testing](https://docs.streamlit.io/)

---

**Happy Testing!** 🎭

