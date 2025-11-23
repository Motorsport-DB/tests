# MotorsportDB Tests

Welcome to the MotorsportDB Tests repository! This project is dedicated to ensuring the quality and reliability of the MotorsportDB application through a comprehensive suite of automated tests.

## Test Types

### 1. Default Tests
The default tests are designed to verify the basic functionality of the application. These tests include:
- Cloning the repository.
- Deploying the application in a Docker container.
- Verifying that the website is accessible.

### 2. Multi Tests
The multi tests provide an extensive validation of the application by checking all pages and various aspects of the system. These tests include:
- **Error Checking**: Ensures there are no errors on any page (`check-errors-motorsportdb`).
- **Broken Links**: Verifies that there are no broken links (`link-motorsportdb`).
- **Unused Images**: Checks for unused images in the project (`unused-picture-motorsportdb`).
- **Date Validation**: Ensures that all dates are correct (`verify-date-motorsportdb`).
- **JSON Structure**: Validates the structure of JSON files (`verify-key-motorsportdb`).

### 3. Validation Warnings
- **Photos & Countries** : Script that lists missing photos and countries as warnings (non-blocking).

## 🏃 Quick Start

### Run Individual Tests
```bash
# Multi tests (all pages)
cd tests/multi/check-errors-motorsportdb && python3 test.py
cd tests/multi/link-motorsportdb && python3 test.py
cd tests/multi/verify-key-motorsportdb && python3 test.py

# Validation warnings
python3 tests/single/validate_photos_countries/test.py
```

## Pre-requisites
- **Docker**: Ensure you have Docker installed and running on your machine.
- **Python 3.8+**: The tests are written in Python.
- **Selenium & ChromeDriver**: For browser automation.
- **Required Python packages**:
  ```bash
  pip install selenium beautifulsoup4 requests
  ```
- **Jenkins** (optional): You may deploy this test on a Jenkins container.

## How to Run the Tests
1. Clone the repository:
    ```bash
    git clone https://github.com/Motorsport-DB/tests.git
    ```
2. Navigate to the project directory:
    ```bash
    cd motorsportdb-tests
    ```
3. Run the desired test suite using the provided scripts.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the tests or add new ones.

When adding new tests:
1. Create a folder in `single/` or `multi/`
2. Follow the existing test structure

Happy testing!  