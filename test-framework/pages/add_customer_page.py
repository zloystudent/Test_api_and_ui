import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Union

class AddCustomerPage(BasePage):
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="First Name"]')
    LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Last Name"]')
    POST_CODE_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Post Code"]')
    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')

    @allure.step("Fill customer form with First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}")
    def fill_customer_form(self, first_name: str, last_name: str, post_code: str) -> 'AddCustomerPage':
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.POST_CODE_INPUT, post_code)
        self.take_screenshot("filled_customer_form")

    @allure.step("Verify form inputs - First Name: {first_name}, Last Name: {last_name}, Post Code: {post_code}")
    def verify_form_inputs(self, first_name: str, last_name: str, post_code: str) -> 'AddCustomerPage':
        first_name_value = self.get_element_value(self.FIRST_NAME_INPUT)
        last_name_value = self.get_element_value(self.LAST_NAME_INPUT)
        post_code_value = self.get_element_value(self.POST_CODE_INPUT)
        
        assert first_name_value == first_name, f"Expected First Name: '{first_name}', but got '{first_name_value}'"
        assert last_name_value == last_name, f"Expected Last Name: '{last_name}', but got '{last_name_value}'"
        assert post_code_value == post_code, f"Expected Post Code: '{post_code}', but got '{post_code_value}'"
            

    @allure.step("Submit customer form")
    def submit_form(self) -> str:
        self.click_element(self.ADD_CUSTOMER_BUTTON)
        alert_text = self.wait_for_alert_and_accept()
        allure.attach(alert_text, name="Alert Text", attachment_type=allure.attachment_type.TEXT)
        return alert_text