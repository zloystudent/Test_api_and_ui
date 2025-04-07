import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import List, Union, Optional

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(15)
        self.wait: WebDriverWait = WebDriverWait(driver, 15, poll_frequency=1)

    @allure.step("Find element with locator: {locator}")
    def find_element(self, locator: Union[str, tuple[By, str]]) -> WebElement:
        return self.driver.find_element(*locator)

    @allure.step("Find elements with locator: {locator}")
    def find_elements(self, locator: Union[str, tuple[By, str]]) -> List[WebElement]:
        return self.driver.find_elements(*locator)

    @allure.step("Click element with locator: {locator}")
    def click_element(self, locator: Union[str, tuple[By, str]]) -> None:
        element: WebElement = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Input text: '{text}' into element with locator: {locator}")
    def input_text(self, locator: Union[str, tuple[By, str]], text: str) -> None:
        element: WebElement = self.wait.until(EC.element_to_be_clickable(locator))
        element.send_keys(text)

    @allure.step("Get value from element with locator: {locator}")
    def get_element_value(self, locator: Union[str, tuple[By, str]]) -> Optional[str]:
        return self.find_element(locator).get_attribute("value")

    @allure.step("Wait for alert, get text and accept")
    def wait_for_alert_and_accept(self) -> str:
        alert = self.wait.until(EC.alert_is_present())
        alert_text: str = alert.text
        alert.accept()
        return alert_text
        
    @allure.step("Take screenshot")
    def take_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )