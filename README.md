# SauceDemo Automation Framework

## PREREQUISITE

Ensure that chromedriver is available at: "C:\chromedriver\chromedriver.exe"

## Installation

### 1. Clone and Navigate to Project Directory

cd <folder_path_where_cloned>/RobotFramework_test


### 2. Create Virtual Environment

python -m venv venv


### 3. Activate Virtual Environment

.\venv\Scripts\activate.bat

### 4. Install Dependencies

pip install -r requirements.txt

## Running Tests

### Run All Tests

pytest

### Run Tests by Marker
pytest -m login

### Run Specific Test

#### LOGIN

- pytest tests/test_login.py::TestLogin::test_successful_login
- pytest tests/test_login.py::TestLogin::test_login_failed

#### FORM SUBMISSION

- pytest tests/test_form_submission.py::TestFormSubmission::test_product_add_and_checkout

## Test Reports

### HTML Report

After running tests, open the HTML report:
```
reports/report.html
```

### Screenshots

Failed test screenshots are automatically saved to:
```
reports/screenshots/
```
