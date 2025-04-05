import os
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from api.entity_api import EntityAPI
from utils.data_generator_for_api import generate_entity_data

from typing import Generator


def pytest_addoption(parser) -> None:
    parser.addoption(
        "--browser", default="chrome", help="Browser to run tests (chrome or firefox)"
    )
    parser.addoption(
        "--mode", default="local", help="Mode to run tests (remote or local)"
    )
    parser.addoption(
        "--app-url",
        default="http://localhost:8080",
        help="Base URL for the application API",
    )


@pytest.fixture
def app_url(request):
    return request.config.getoption("--app-url")


@pytest.fixture
def api_client(app_url):
    with allure.step("Initialize API client"):
        client = EntityAPI(base_url=app_url)
        allure.attach(app_url, "Base URL")
        return client


@pytest.fixture
def json_data():
    with allure.step("Generate test data"):
        data = generate_entity_data()
        allure.attach(str(data), "Generated Test Data")
        return data


@pytest.fixture
def json_data_for_patch():
    with allure.step("Generate test data for update"):
        data = generate_entity_data()
        allure.attach(str(data), "Generated Test Data for Update")
        return data


@pytest.fixture
def created_entity_id(api_client, json_data):
    with allure.step("Setup: Create entity for testing"):
        entity_id = api_client.create_entity(json_data)
        allure.attach(str(entity_id), "Created Entity ID")

    yield entity_id

    with allure.step(f"Teardown: Delete entity with ID {entity_id}"):
        try:
            api_client.delete_entity(entity_id)
        except Exception as e:
            allure.attach(
                str(e), "Exception during entity cleanup", allure.attachment_type.TEXT
            )

            pass


# UI фикстуры
@pytest.fixture(scope="function")
def driver(request) -> Generator[webdriver.Remote, None, None]:
    browser = request.config.getoption("--browser")
    mode = request.config.getoption("--mode")

    is_remote = mode.lower() == "remote"

    if not is_remote:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.page_load_strategy = "eager"

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        original_browser = browser
        browser = "chrome"

        allure.attach(
            f"Browser: Chrome (requested: {original_browser})\n"
            f"Mode: Local\n"
            f"Options: {chrome_options.arguments}",
            name="Browser Configuration",
            attachment_type=allure.attachment_type.TEXT,
        )

    else:
        if browser == "chrome":
            chrome_options = ChromeOptions()
            if os.environ.get("HEADLESS", "false").lower() == "true":
                chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.page_load_strategy = "eager"

            selenium_hub_host = os.environ.get("SELENIUM_HUB_HOST", "selenium-hub")
            selenium_hub_port = os.environ.get("SELENIUM_HUB_PORT", "4444")
            selenium_grid_url = f"http://{selenium_hub_host}:{selenium_hub_port}/wd/hub"

            driver = webdriver.Remote(
                command_executor=selenium_grid_url, options=chrome_options
            )

            allure.attach(
                f"Browser: Chrome\nMode: Remote\nOptions: {chrome_options.arguments}",
                name="Browser Configuration",
                attachment_type=allure.attachment_type.TEXT,
            )

        elif browser == "firefox":
            firefox_options = FirefoxOptions()
            if os.environ.get("HEADLESS", "false").lower() == "true":
                firefox_options.add_argument("--headless")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference(
                "browser.download.manager.showWhenStarting", False
            )
            firefox_options.page_load_strategy = "eager"

            selenium_hub_host = os.environ.get("SELENIUM_HUB_HOST", "selenium-hub")
            selenium_hub_port = os.environ.get("SELENIUM_HUB_PORT", "4444")
            selenium_grid_url = f"http://{selenium_hub_host}:{selenium_hub_port}/wd/hub"

            driver = webdriver.Remote(
                command_executor=selenium_grid_url, options=firefox_options
            )

            allure.attach(
                f"Browser: Firefox\nMode: Remote\nOptions: {firefox_options.arguments}",
                name="Browser Configuration",
                attachment_type=allure.attachment_type.TEXT,
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()

    request.node._browser = browser
    request.node._mode = mode

    test_name = request.node.name
    allure.dynamic.title(f"{test_name} - {browser.capitalize()} ({mode})")

    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG,
        )

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call) -> None:
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    if rep.failed:
        allure.attach(
            str(call.excinfo),
            name="Exception Info",
            attachment_type=allure.attachment_type.TEXT,
        )
