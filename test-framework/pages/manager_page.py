import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Type

class ManagerPage(BasePage):
    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, 'button[ng-class="btnClass1"]')
    CUSTOMERS_BUTTON = (By.CSS_SELECTOR, 'button[ng-class="btnClass3"]')

    def __init__(self, driver):
        super().__init__(driver)
        self.url: str = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/manager"

    @allure.step("Navigate to Manager Page")
    def navigate_to(self) -> 'ManagerPage':
        self.driver.get(self.url)
        return self

    @allure.step("Click Add Customer button")
    def click_add_customer(self) -> 'AddCustomerPage':
        self.click_element(self.ADD_CUSTOMER_BUTTON)
        from pages.add_customer_page import AddCustomerPage
        return AddCustomerPage(self.driver)

    @allure.step("Click Customers button")
    def click_customers(self) -> 'CustomersPage':
        self.click_element(self.CUSTOMERS_BUTTON)
        from pages.customers_page import CustomersPage
        return CustomersPage(self.driver)