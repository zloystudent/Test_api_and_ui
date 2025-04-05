import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List, Optional

class CustomersPage(BasePage):
    SORT_BY_NAME_BUTTON = (By.XPATH, '//*[contains(@ng-click, "fName")]')
    CUSTOMERS_TABLE = (By.CSS_SELECTOR, 'table[class="table table-bordered table-striped"]')
    TABLE_ROWS = (By.TAG_NAME, "tr")
    TABLE_COLUMNS = (By.TAG_NAME, "td")
    DELETE_BUTTONS = (By.XPATH, "//*[@ng-click='deleteCust(cust)']")

    @allure.step("Sort customers by name")
    def sort_by_name(self) -> 'CustomersPage':
        self.click_element(self.SORT_BY_NAME_BUTTON)
        self.take_screenshot("sorted_customers")

    @allure.step("Get first column data from customers table")
    def get_first_column_data(self) -> List[str]:
        table = self.find_element(self.CUSTOMERS_TABLE)
        rows = table.find_elements(*self.TABLE_ROWS)
        rows = rows[1:]

        first_column_data = []
        for row in rows:
            cells = row.find_elements(*self.TABLE_COLUMNS)
            if cells:
                first_cell = cells[0]
                first_column_data.append(first_cell.text)

        allure.attach(
            "\n".join(first_column_data), 
            name="Customer Names", 
            attachment_type=allure.attachment_type.TEXT
        )
        return first_column_data

    @allure.step("Verify customers are sorted in descending order")
    def verify_descending_sort(self) -> 'CustomersPage':
        first_column_data = self.get_first_column_data()
        sorted_data = sorted(first_column_data, key=str.lower, reverse=True)

        with allure.step(f"Compare actual order with expected descending order"):
            assert first_column_data == sorted_data


    @allure.step("Delete first customer with average name length")
    def delete_customers_with_average_name_length(self) -> List[str]:
        first_column_data = self.get_first_column_data()

        name_lengths = [len(name) for name in first_column_data]
        with allure.step("Calculate average name length"):
            average_length = sum(name_lengths) / len(name_lengths) if name_lengths else 0
            allure.attach(f"{average_length:.2f}", name="Average length", attachment_type=allure.attachment_type.TEXT)


        nearest_length = min(name_lengths, key=lambda x: abs(x - average_length))

        # Find only the first index with the nearest length
        index_to_delete: Optional[int] = next((i for i, length in enumerate(name_lengths) if length == nearest_length), None)

        with allure.step(f"Found name with length {nearest_length} closest to average"):
            if index_to_delete is not None:
                allure.attach(
                    f"Index {index_to_delete}: {first_column_data[index_to_delete]}",
                    name="Name to delete",
                    attachment_type=allure.attachment_type.TEXT
                )

        delete_buttons = self.find_elements(self.DELETE_BUTTONS)
        expected_names = first_column_data.copy()

        if index_to_delete is not None and index_to_delete < len(delete_buttons):
            with allure.step(f"Delete customer at index {index_to_delete}: {expected_names[index_to_delete]}"):
                delete_buttons[index_to_delete].click()
                del expected_names[index_to_delete]

        self.take_screenshot("after_deletion")
        return expected_names

    @allure.step("Verify customer deletion")
    def verify_deletion(self, expected_names: List[str]) -> 'CustomersPage':
        current_names = self.get_first_column_data()

        with allure.step("Compare current customer list with expected list after deletion"):
            assert set(expected_names) == set(current_names)
