# Playwright Python SauceDemo Tests

This project contains end-to-end UI tests for [Swag Labs (SauceDemo)](https://www.saucedemo.com/) using `pytest-playwright`.

## Prerequisites

- Python 3.8+ (project currently uses Python 3.14)
- Windows PowerShell

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install
```

## Run Tests

Default test run opens the browser UI (headed mode), runs on Chromium (Chrome engine), and writes Allure results:

```powershell
.\.venv\Scripts\python -m pytest -q
```

Useful run options:

- Run with visible browser and slow down interactions:
  ```powershell
  .\.venv\Scripts\python -m pytest -q --slowmo 400
  ```
- Run in headless mode (override default):
  ```powershell
  .\.venv\Scripts\python -m pytest -q --headless
  ```
- Run on Firefox instead of the default Chromium:
  ```powershell
  .\.venv\Scripts\python -m pytest -q --browser firefox
  ```

## New Scenario Test

`test_saucedemo_top4_expensive_cart.py` covers this flow:

- Login with `standard_user` / `secret_sauce`
- Select the 4 most expensive inventory items
- Wait `1100ms` between each item selection
- Calculate expected total from inventory prices
- Verify the cart total matches the expected total
- Wait `3000ms` at the end and keep browser open (no explicit `page.close()`)

Run only this test:

```powershell
.\.venv\Scripts\python -m pytest -q test_saucedemo_top4_expensive_cart.py
```

Run this test on Firefox:

```powershell
.\.venv\Scripts\python -m pytest -q test_saucedemo_top4_expensive_cart.py --browser firefox
```

## Allure Reports

Test runs generate results in `allure-results/`.

If Allure CLI is installed:

```powershell
allure serve allure-results
```

Or generate static report:

```powershell
allure generate allure-results -o allure-report --clean
```

## GitHub Actions (Auto Test Run)

This project includes a CI workflow at `.github/workflows/tests.yml` that runs automatically on:

- Push to `main`
- Pull requests targeting `main`
- Manual trigger from the Actions tab (`workflow_dispatch`)

The workflow runs the suite headless on both Chromium and Firefox.

## Test Data

- Accepted users are stored in `test_data/accepted_users.json`
- Password for accepted users: `secret_sauce`
