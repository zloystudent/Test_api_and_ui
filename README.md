URL Allure Report https://zloystudent.github.io/Test_api_and_ui/

# API Service
This service provides access points for managing entities in a PostgreSQL database. It includes a Docker Compose configuration for setting up the service, database, and migrations.

Getting Started
Clone this repository.
Install Docker and Docker Compose if they are not already installed.

Usage
To run the service, database, and migrations, navigate to the project directory and execute:

`make run` or `docker-compose up --build -d`

## API Endpoints

- Create entity: POST /api/create
- Delete entity: DELETE /api/delete/{id}
- Get entity: GET /api/get/{id}
- Get all entities: GET /api/getAll
- Update entity: PATCH /api/patch/{id}

#### HOST http://localhost:8080

#### SWAGGER documentation http://localhost:8080/api/\_/docs/swagger/

# Automated API and UI Testing Framework

To start, go to the folder test-framework

## Table of Contents

- Overview
- Requirements
- Project Structure
- Setup
- Running Tests
- Local Execution
- Docker Execution
- Test Configuration
- Viewing Allure Reports
- Test Examples
- Supported Browsers
- Troubleshooting

## Overview

This project is a comprehensive automated testing framework that enables both API and UI testing. The framework utilizes:

- Pytest - as the primary testing framework
- Selenium WebDriver - for UI automation testing
- Allure - for detailed test execution reporting
- Docker - for parallel test execution across various browsers (Chrome, Firefox, Edge)
- Selenium Grid - for distributed test execution
  The framework supports both local test execution and remote execution via Selenium Grid, allowing for scalable testing and cross-browser validation.

## Requirements

For local execution:

- Python 3.8+
- Pip
- Chrome/Firefox browsers
  For Docker execution:
- Docker
- Docker Compose

## Project Structure

```
project/
│
├── api/                      # API clients and methods
│   └── entity_api.py         # Client for Entity API operations
│
├── models/                   # Data models
│   └── entity_models.py      # Pydantic models for Entity API
│
├── pages/                    # Page Objects for UI tests
│   ├── add_customer_page.py  # Page Object for add_ customer page
│   ├── base_page.py          # Page Object for base page
│   ├── customers_page.py     # Page Object for customers page
│   └── manager_page.py       # Page Object for manager page
│
├── tests/                    # Tests
│   ├── api/                  # API tests
│   │   └── test_entity_api.py # Entity API tests
│   │
│   └── ui/                   # UI tests
│       └── test_customers_ui.py # Customer UI tests
│
├── utils/                    # Utility functions
│   ├── allure_environment.py # Help-functions for allure reports
│   ├── allure_utils.py       # Help-functions for allure reports
│   ├── data_generator.py     # Test data generator for UI
│   └── data_generator_for_api.py # Test data generator for API
│
├── videos/                   # Directory for test videos
│   ├── chrome/               # Chrome test videos
│   ├── firefox/              # Firefox test videos
│   └── edge/                 # Edge test videos
│
├── allure-results/           # Test results for Allure
├── allure-reports/           # Generated Allure reports
│
├── conftest.py               # Pytest configuration, fixtures
├── constants.py              # Project constants
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── pytest.ini                # Pytest settings
├── docker-compose.yml        # Docker Compose configuration
└── Dockerfile                # Dockerfile for test container

```

## Installation

### Local Setup

1.  Clone the repository:

```
git clone <repository-url>
cd <project-folder>
```

2.  Create and activate a virtual environment:

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate or .\venv\Scripts\Activate.ps1
```

3.  Install dependencies:

```
pip install -r requirements.txt
```

## Docker Setup

No additional installation is needed beyond Docker and Docker Compose.

## Running Tests

### Locally

Run tests using pytest directly:

```
# Run all tests with Chrome browser in local mode
pytest

# Run specific test file
pytest tests/ui/test_customer_management.py --mode local

#To run API tests:
pytest -v -m api --app-url=http://your-api-host:port

#To run UI tests:
pytest -v -m ui

# Run with Allure reporting
pytest --alluredir=./allure-results
```

### Using Docker Compose

Run tests in a containerized environment with Selenium Grid:

```
# To run all tests in Docker:
docker-compose up -d pytest-chrome pytest-firefox pytest-edge pytest-api

# Run only Chrome tests
docker-compose up -d pytest-chrome

# Run only Firefox tests
docker-compose up -d pytest-firefox

# Run specific test path with Chrome
TEST_PATH=tests/test_customer_management.py docker-compose up -d pytest-chrome

# Control parallel instances
CHROME_INSTANCES=5 docker-compose up -d pytest-chrome
```

## Viewing Test Results

Allure reports are available at http://localhost:5050 after running tests with Docker Compose.
To generate and view Allure reports locally:

```
# Generate report from results
allure generate allure-results -o allure-report

# Open the report
allure open allure-report
```

## Configuration Options

### Command Line Options

- --browser: Specify browser (chrome or firefox)
- --mode: Execution mode (local or remote)
- --app-url - base URL for the application/API

## Environment Variables

When running in Docker:

- SELENIUM_HUB_HOST: Selenium hub hostname (default: selenium-hub)
- SELENIUM_HUB_PORT: Selenium hub port (default: 4444)
- HEADLESS: Run browsers in headless mode (true/false)
- CHROME_INSTANCES: Number of parallel Chrome test instances
- FIREFOX_INSTANCES: Number of parallel Firefox test instances
- TEST_PATH: Specific test path to run

## Test Examples

### API Test Example

```
@pytest.mark.api
@allure.epic("Entity API")
@allure.feature("Entity CRUD Operations")
class TestEntityAPI:
    @allure.story("Entity Creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test creating a new entity and verifying it exists")
    def test_create_entity(self, api_client, json_data):
        with allure.step("Create new entity with test data"):
            entity_id = api_client.create_entity(json_data)

        # Additional test steps
```

### UI Test Example

```
@pytest.mark.ui
@allure.epic("Customer UI")
@allure.feature("Customer Management")
@allure.story("Add and Manage Customers")
class TestCustomersUI:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test adding a new customer")
    @allure.title("Test adding a new customer")
    def test_add_customers(self, driver: WebDriver) -> None:
        with allure.step("Generate test data"):
            post_code = DataGenerator.generate_random_post_code()
            # Additional data generation

        # Additional test steps

```

## Supported Browsers

- Chrome - fully supported in both local and remote mode
- Firefox - supported only in remote mode via Selenium Grid
- Edge - supported only in remote mode via Selenium Grid
