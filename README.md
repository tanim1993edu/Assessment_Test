Automation Framework

[![Assessment Test Workflow](https://github.com/tanim1993edu/Assessment_Test/actions/workflows/assessment-workflow.yml/badge.svg)](https://github.com/tanim1993edu/Assessment_Test/actions/workflows/assessment-workflow.yml)

This repository contains the automation framework. implementing both UI and API tests for [Automation Exercise](https://automationexercise.com).

This repository contains a comprehensive Playwright + pytest automation framework
for the [Automation Exercise](https://automationexercise.com) practice site. 
It demonstrates enterprise-level test automation practices including:

✨ **Core Features**
- Page Object Model architecture
- API and UI test integration
- Cross-browser testing (Chrome, Firefox)
- Parallel test execution
- Comprehensive reporting
- CI/CD pipeline integration

🎯 **Test Coverage**
- End-to-end purchase workflow
- API account creation and validation
- Invoice download verification
- Error scenarios and edge cases

📊 **Quality Assurance**
- Automated test reports
- Screenshot capture on failure
- Comprehensive logging
- Cross-browser validation

## Project Structure

The framework follows a modular structure:

```
automation/
├── pages/                  # Page Object Model classes
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   ├── payment_page.py
│   └── order_confirmation_page.py
├── tests/                  # API and UI tests
│   ├── test_api_create_account.py
│   └── test_end_to_end_purchase.py
├── utils/                  # Config and test data helpers
│   ├── config.py
│   └── test_data.py
├── conftest.py             # Pytest fixtures for browsers and contexts
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── user_credentials.json   # Persisted credentials between API and UI tests
└── README.md               # This file
```

## Getting Started Locally

1. **Clone the repository** and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**. Run the following to install the required packages and the Playwright browsers:

   ```bash
   pip install -r requirements.txt
   playwright install
   ```

3. **Run the API and UI tests**. The API test will create a unique user and save the credentials to `user_credentials.json`. The UI test will then log in with the same credentials, purchase products, and download an invoice.

   ```bash
   pytest -v -s
   ```

4. **Parallel and cross‑browser execution**. You can run the tests in parallel across multiple browsers by specifying the `-n` flag and passing different browser names via environment variables:

   ```bash
   # Run all tests in parallel on Chromium and Firefox
   export BROWSERS=chromium,firefox
   pytest -n auto
   ```

   To run on a single browser, set `BROWSERS` to the desired value:

   ```bash
   export BROWSERS=firefox
   pytest
   ```

5. **Reports and logs**. Logging is configured via Python's `logging` module. You can customise log location and verbosity by modifying `automation/utils/config.py`. Test reports can be generated with a plugin such as [`pytest‑html`](https://pypi.org/project/pytest-html/). To enable HTML reporting run:

   ```bash
   pip install pytest-html
   pytest --html=report.html --self-contained-html
   ```

## CI/CD Integration

The framework includes a robust GitHub Actions workflow (`.github/workflows/test.yml`) that provides:

### 🔄 Automated Workflow
- Triggers on:
  - Push to main/master
  - Pull requests
  - Manual workflow dispatch
- Matrix testing across browsers
- Parallel test execution
- Comprehensive artifact collection

### 📦 Published Artifacts
- HTML test reports
- Failure screenshots
- Test execution logs
- Downloaded invoices
- Browser HAR files

### 🎛 Configurable Options
When triggering manually, you can configure:
- Browser selection (Chrome/Firefox)
- Headed/Headless mode
- Custom test parameters

### 📊 Latest Test Results
View the latest test runs and artifacts here:
[GitHub Actions Dashboard](https://github.com/tanim1993edu/Assessment_Test/actions)

Example successful run with artifacts:
[Test Run #11](https://github.com/tanim1993edu/Assessment_Test/actions/runs/6790600643)

### 🏷 Build Status
[![Assessment Test](https://github.com/tanim1993edu/Assessment_Test/actions/workflows/test.yml/badge.svg)](https://github.com/tanim1993edu/Assessment_Test/actions/workflows/test.yml)

## Test Data Management

Unique user data is generated at runtime using helpers in
`utils/test_data.py`. The API test registers a new user via the
`/api/createAccount` endpoint, persists the credentials to
`user_credentials.json`, and the UI test subsequently reads those
credentials to log in through the web UI. This ensures repeatability and
isolation between runs without polluting the database with static test
accounts.

## Notes & Limitations

* **Network Constraints**: If the `createAccount` API is inaccessible
  from your network (for example due to CORS or firewall restrictions),
  the API tests may fail. In such cases you can manually populate
  `user_credentials.json` with an existing user and skip the API test.

* **Selectors**: The CSS selectors provided in the page objects are
  based on the current markup of the Automation Exercise website. If
  elements change, you may need to update the selectors accordingly.

* **Payments**: The payment details used in the UI test are dummy
  values appropriate for a test environment. Do **not** supply real
  credit card information in this framework.

## Test Execution Guide

### 🌐 Browser Options

The framework supports multiple browsers through Playwright:

```bash
# Run on specific browser
pytest --browser chromium
pytest --browser firefox

# Run in headed mode
pytest --headed

# Run specific test file
pytest tests/test_end_to_end_purchase.py

# Run with specific markers
pytest -m "api"  # API tests only
pytest -m "ui"   # UI tests only
```

### ⚡ Parallel Execution

Run tests in parallel using pytest-xdist:

```bash
# Auto-detect CPU count
pytest -n auto

# Specify number of workers
pytest -n 4
```

### 📊 Reporting Options

Generate and customize test reports:

```bash
# Generate HTML report
pytest --html=reports/report.html

# Include screenshots in report
pytest --html=reports/report.html --self-contained-html

# Detailed console output
pytest -v --tb=short
```

### 🔄 Retry Options

Handle flaky tests with automatic retries:

```bash
# Retry failed tests
pytest --reruns 2

# Retry with delay
pytest --reruns 2 --reruns-delay 1
```

## Retrying Flaky Tests

Pytest's `--reruns` option can be used to automatically retry tests
that intermittently fail. This framework includes a default of `0`
retries in `pytest.ini` but you can override it on the command line:

```bash
pytest --reruns 2
```

## Cleaning Up

The downloads and logs directories are automatically created under
`automation/downloads` and `automation/logs`. You can safely delete
these directories between runs to clean up generated artefacts.
