# Test Execution Cheat Sheet

## Local Test Execution Commands

### Browser Selection

```bash
# Run in Chromium
$env:BROWSERS='chromium'; pytest

# Run in Firefox
$env:BROWSERS='firefox'; pytest

# Run in both browsers
$env:BROWSERS='chromium,firefox'; pytest
```

### Headed vs Headless Mode

```bash
# Run in headed mode (visible browser)
$env:HEADLESS='false'; pytest

# Run in headless mode (invisible browser)
$env:HEADLESS='true'; pytest

# Combined browser and mode selection
$env:BROWSERS='chromium'; $env:HEADLESS='false'; pytest
```

### Running Specific Tests

```bash
# Run single test file
pytest tests/test_end_to_end_purchase.py

# Run specific test by name
pytest -k "test_end_to_end_purchase"

# Run API tests only
pytest tests/test_api_create_account.py tests/test_api_negative.py

# Run UI tests only
pytest tests/test_end_to_end_purchase.py tests/test_login.py
```

### Parallel Execution

```bash
# Run tests in parallel
pytest -n auto

# Run with specific number of workers
pytest -n 2

# Parallel execution with browser selection
$env:BROWSERS='chromium,firefox'; pytest -n 2
```

### Report Generation

```bash
# Generate HTML report
pytest --html=reports/report.html

# Generate report with screenshots
pytest --html=reports/report.html --self-contained-html

# Run with detailed console output
pytest -v --tb=short
```

## Common Scenarios

### 1. Full End-to-End Test in Headed Mode
```bash
# Single command
$env:PYTHONPATH = $PWD; $env:BROWSERS='chromium'; $env:HEADLESS='false'; pytest -v

# Or step by step:
$env:PYTHONPATH = $PWD
$env:BROWSERS='chromium'
$env:HEADLESS='false'
pytest -v
```

### 2. Single Test in Headed Mode
```bash
# Run specific test in headed Chromium
$env:PYTHONPATH = $PWD
$env:BROWSERS='chromium'
$env:HEADLESS='false'
pytest tests/test_end_to_end_purchase.py -v
```

### 3. Push and Run in CI/CD
```bash
# Add changes
git add .

# Commit with descriptive message
git commit -m "Add new test for feature X"

# Push to trigger CI/CD
git push

# View results in GitHub Actions:
# https://github.com/tanim1993edu/Assessment_Test/actions
```

### 4. Debug Mode with Screenshots
```bash
# Run with screenshot capture on failure
$env:BROWSERS='chromium'
$env:HEADLESS='false'
pytest --html=reports/debug_report.html --self-contained-html
```

### 5. Cross-Browser Testing
```bash
# Run same test across browsers
$env:BROWSERS='chromium,firefox'
$env:HEADLESS='true'
pytest tests/test_end_to_end_purchase.py -v

# Run in parallel
$env:BROWSERS='chromium,firefox'
pytest -n 2
```

### 6. Test with Different Environments
```bash
# Development environment
$env:BASE_URL='https://dev.automationexercise.com'
pytest

# Staging environment
$env:BASE_URL='https://staging.automationexercise.com'
pytest
```

### 7. Performance Testing Mode
```bash
# Run with timing data
pytest --durations=0

# Run with trace
$env:PWDEBUG=1
pytest
```

## Debugging Commands

### 1. Show Browser
```bash
# Run with visible browser and slow motion
$env:HEADLESS='false'
$env:SLOW_MO=1000
pytest
```

### 2. Debug Logging
```bash
# Increase log level
pytest --log-cli-level=DEBUG

# Show test output
pytest -s
```

### 3. Interactive Debug
```bash
# Break on failure
pytest --pdb

# Debug with trace viewer
$env:PWDEBUG=1
pytest
```

## CI/CD Specific Commands

### 1. View Workflow Status
```bash
# Check workflow status
gh workflow list

# View last run
gh run list --limit 1
```

### 2. Download Artifacts
```bash
# Download latest artifacts
gh run download

# Download specific artifact
gh run download --name test-results
```

### 3. Trigger Manual Run
```bash
# Trigger workflow
gh workflow run test.yml

# Trigger with inputs
gh workflow run test.yml -f browsers=chromium -f headless=false
```

## Best Practices

1. Always set PYTHONPATH before running tests:
```bash
$env:PYTHONPATH = $PWD
```

2. Clean up before runs:
```bash
# Remove old reports
Remove-Item reports/* -Recurse -Force
Remove-Item downloads/* -Recurse -Force
```

3. Check test environment:
```bash
# Verify Python path
python -c "import sys; print(sys.path)"

# Check browser installation
playwright install --with-deps chromium firefox
```

4. Review results:
```bash
# Open latest report
Start-Process reports/report*.html

# Check screenshots
explorer.exe reports\screenshots
```