# 🛒 E-commerce Test Automation Framework (Python)

A complete Selenium WebDriver + pytest automation framework for testing e-commerce applications. Built with Page Object Model (POM) design pattern and Python best practices.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.15.0-green)
![pytest](https://img.shields.io/badge/pytest-7.4.3-red)

---

## 📋 Table of Contents
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup Instructions](#-setup-instructions)
- [Running Tests](#-running-tests)
- [Test Reports](#-test-reports)
- [Configuration](#-configuration)
- [Author](#-author)

---

## ✨ Features

- ✅ **Page Object Model (POM)** - Clean separation of test logic and page interactions
- ✅ **pytest Framework** - Powerful test configuration, fixtures, and parallel execution
- ✅ **HTML Reports** - Beautiful HTML test reports with screenshots on failure
- ✅ **WebDriver Manager** - Automatic browser driver management
- ✅ **Cross-Browser Support** - Chrome, Firefox, Edge
- ✅ **Explicit Waits** - Robust wait utilities for stable tests
- ✅ **Configuration Driven** - Easy test configuration via config.ini file
- ✅ **Markers** - Organize tests with smoke, regression, and module markers
- ✅ **Screenshots on Failure** - Automatic screenshot capture when tests fail

---

## 📁 Project Structure

```
ecommerce-test-framework-python/
├── config.ini                    # Test configuration
├── pytest.ini                    # pytest configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Common page methods
│   ├── login_page.py             # Login page actions
│   ├── products_page.py          # Products page actions
│   ├── cart_page.py              # Cart page actions
│   └── checkout_page.py          # Checkout page actions
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures
│   ├── test_login.py             # Login test cases
│   ├── test_products.py          # Product test cases
│   ├── test_cart.py              # Cart test cases
│   └── test_checkout.py          # Checkout test cases
├── utils/
│   ├── __init__.py
│   ├── config_reader.py          # Config file reader
│   └── wait_helper.py            # Explicit wait utilities
├── reports/                      # Generated HTML reports
└── screenshots/                  # Failure screenshots
```

---

## 🔧 Prerequisites

Before running the tests, ensure you have:

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

3. **Chrome/Firefox/Edge browser installed**

4. **Git** (to clone the repository)

---

## 🚀 Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/shivansh-77/ecommerce-test-framework-python.git
cd ecommerce-test-framework-python
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup
```bash
pytest --version
```

---

## ▶️ Running Tests

### Run All Tests
```bash
pytest
```

### Run with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_login.py
pytest tests/test_products.py
pytest tests/test_cart.py
pytest tests/test_checkout.py
```

### Run Specific Test Function
```bash
pytest tests/test_login.py::TestLogin::test_valid_login
```

### Run Tests by Marker
```bash
# Run only smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run login module tests
pytest -m login

# Run products module tests
pytest -m products

# Run cart module tests
pytest -m cart

# Run checkout module tests
pytest -m checkout
```

### Run Tests in Parallel (faster)
```bash
pip install pytest-xdist
pytest -n 4  # Run on 4 CPU cores
```

### Run in Headless Mode
Edit `config.ini`:
```ini
headless = true
```
Then run tests normally.

### Run on Different Browser
Edit `config.ini`:
```ini
browser = firefox    # or chrome, edge
```

---

## 📊 Test Reports

After running tests, reports are generated in:

### HTML Report
```
reports/report.html
```
Open this file in any browser for a detailed test report.

### Screenshot on Failure
```
screenshots/<test_name>.png
```

### Generate Allure Report (Optional)
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

---

## ⚙️ Configuration

All configurations are in `config.ini`:

```ini
[settings]
base_url = https://www.saucedemo.com
browser = chrome
headless = false
implicit_wait = 10
explicit_wait = 15

[credentials]
valid_username = standard_user
valid_password = secret_sauce
invalid_username = invalid_user
invalid_password = wrong_password
locked_username = locked_out_user

[paths]
screenshot_path = screenshots/
report_path = reports/
```

---

## 📝 Test Cases Overview

| Module    | Test Cases | Description |
|-----------|------------|-------------|
| Login     | 8 tests    | Valid/invalid login, empty fields, locked user |
| Products  | 11 tests   | Display, add to cart, sorting, logout |
| Cart      | 7 tests    | Add/remove items, persistence, navigation |
| Checkout  | 10 tests   | Form validation, E2E order flow |

**Total: 36 Test Cases**

---

## 🧪 Test Application

This framework tests [SauceDemo](https://www.saucedemo.com) - a sample e-commerce site designed for testing practice.

**Available Test Users:**
- `standard_user` - Normal user
- `locked_out_user` - Locked account
- `problem_user` - Buggy experience
- `performance_glitch_user` - Slow responses

**Password for all:** `secret_sauce`

---

## 💡 Key Concepts Demonstrated

1. **Page Object Model** - Each page has its own class with locators and methods
2. **pytest Fixtures** - Reusable setup/teardown with `conftest.py`
3. **Explicit Waits** - WaitHelper class for stable element interactions
4. **Markers** - Organize and filter tests (smoke, regression)
5. **Configuration Management** - External config file for easy changes
6. **Screenshots on Failure** - Automatic capture via pytest hooks
7. **HTML Reports** - Beautiful reports with pytest-html

---

## 🔄 Extending the Framework

### Adding New Page Object
1. Create new file in `pages/` extending `BasePage`
2. Define locators as tuples: `LOCATOR = (By.ID, "element-id")`
3. Create action methods using inherited helper methods
4. Import in `pages/__init__.py`

### Adding New Tests
1. Create new file in `tests/` following `test_*.py` naming
2. Create test class starting with `Test`
3. Use fixtures from `conftest.py`
4. Add appropriate markers (`@pytest.mark.smoke`, etc.)

---

## 👤 Author

**Shivansh Bajpai**
- GitHub: [@shivansh-77](https://github.com/shivansh-77)
- LinkedIn: [Shivansh Bajpai](https://linkedin.com/in/shivansh-bajpai-522965257/)

---

## 📄 License

This project is open source and available for learning purposes.

---

## 🙏 Acknowledgments

- [SauceDemo](https://www.saucedemo.com) for the test application
- [Selenium](https://www.selenium.dev/) for WebDriver
- [pytest](https://pytest.org/) for test framework
- [pytest-html](https://pytest-html.readthedocs.io/) for reporting

---

⭐ **Star this repo if you find it helpful!**
