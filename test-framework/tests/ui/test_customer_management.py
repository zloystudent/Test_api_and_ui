import pytest
import allure
from pages.manager_page import ManagerPage
from utils.data_generator import DataGenerator
from constants import DEFAULT_LAST_NAME
from selenium.webdriver.remote.webdriver import WebDriver


@pytest.mark.ui
@allure.epic("Customer UI")
@allure.feature("Customer Management")
@allure.story("Add and Manage Customers")
class TestCustomersUI:
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test adding a new customer")
    @allure.title("Test adding a new customer")
    def test_add_customers(self, driver: WebDriver) -> None:
        # Generate test data
        with allure.step("Generate test data"):
            post_code = DataGenerator.generate_random_post_code()
            first_name = DataGenerator.generate_name_from_post_code(post_code)
            last_name = DEFAULT_LAST_NAME

            allure.attach(
                f"First Name: {first_name}\nLast Name: {last_name}\nPost Code: {post_code}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Initialize page objects and navigate to manager page
        with allure.step("Navigate to Manager Page"):
            manager_page = ManagerPage(driver).navigate_to()

        # Add a new customer
        with allure.step("Add a new customer"):
            add_customer_page = manager_page.click_add_customer()
            add_customer_page.fill_customer_form(first_name, last_name, post_code)
            add_customer_page.verify_form_inputs(first_name, last_name, post_code)

        # Submit form and verify alert
        with allure.step("Submit form and verify confirmation alert"):
            alert_text = add_customer_page.submit_form()
            assert "Customer added successfully" in alert_text, (
                f"Expected success message, got: {alert_text}"
            )

    @allure.description("Test adding a new customer, sorting customers by name")
    @allure.title("Test sort customers")
    def test_sort_customers(self, driver: WebDriver) -> None:
        # Generate test data
        with allure.step("Generate test data"):
            post_code = DataGenerator.generate_random_post_code()
            first_name = DataGenerator.generate_name_from_post_code(post_code)
            last_name = DEFAULT_LAST_NAME

            allure.attach(
                f"First Name: {first_name}\nLast Name: {last_name}\nPost Code: {post_code}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Initialize page objects and navigate to manager page
        with allure.step("Navigate to Manager Page"):
            manager_page = ManagerPage(driver).navigate_to()

        # Add a new customer
        with allure.step("Add a new customer"):
            add_customer_page = manager_page.click_add_customer()
            add_customer_page.fill_customer_form(first_name, last_name, post_code)
            add_customer_page.verify_form_inputs(first_name, last_name, post_code)

        # Submit form and verify alert
        with allure.step("Submit form and verify confirmation alert"):
            alert_text = add_customer_page.submit_form()
            assert "Customer added successfully" in alert_text, (
                f"Expected success message, got: {alert_text}"
            )

        # Navigate to customers page
        with allure.step("Navigate to Customers Page"):
            customers_page = manager_page.click_customers()

        # Sort customers by name and verify sorting
        with allure.step("Sort customers by name and verify descending order"):
            customers_page.sort_by_name()
            customers_page.verify_descending_sort()

    @allure.description(
        "Test adding a new customer, sorting customers by name, and deleting customers with average name length"
    )
    @allure.title("Delete customer")
    def test_delete_customers(self, driver: WebDriver) -> None:
        # Generate test data
        with allure.step("Generate test data"):
            post_code = DataGenerator.generate_random_post_code()
            first_name = DataGenerator.generate_name_from_post_code(post_code)
            last_name = DEFAULT_LAST_NAME

            allure.attach(
                f"First Name: {first_name}\nLast Name: {last_name}\nPost Code: {post_code}",
                name="Test Data",
                attachment_type=allure.attachment_type.TEXT,
            )

        # Initialize page objects and navigate to manager page
        with allure.step("Navigate to Manager Page"):
            manager_page = ManagerPage(driver).navigate_to()

        # Add a new customer
        with allure.step("Add a new customer"):
            add_customer_page = manager_page.click_add_customer()
            add_customer_page.fill_customer_form(first_name, last_name, post_code)
            add_customer_page.verify_form_inputs(first_name, last_name, post_code)

        # Submit form and verify alert
        with allure.step("Submit form and verify confirmation alert"):
            alert_text = add_customer_page.submit_form()
            assert "Customer added successfully" in alert_text, (
                f"Expected success message, got: {alert_text}"
            )

        # Navigate to customers page
        with allure.step("Navigate to Customers Page"):
            customers_page = manager_page.click_customers()

        # Sort customers by name and verify sorting
        with allure.step("Sort customers by name and verify descending order"):
            customers_page.sort_by_name()
            customers_page.verify_descending_sort()

        # Delete customers with average name length and verify deletion
        with allure.step(
            "Delete customers with average name length and verify deletion"
        ):
            expected_names = customers_page.delete_customers_with_average_name_length()
            customers_page.verify_deletion(expected_names)
