import requests
import allure
from typing import Dict, Any, Tuple
from utils.allure_utils import allure_request_logger, allure_response_logger


class EntityAPI:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @allure.step("Create a new entity")
    def create_entity(self, data: Dict[str, Any]) -> int:
        """Create a new entity and return its ID."""
        url = f"{self.base_url}/api/create"

        allure_request_logger("POST", url, self.headers, data)

        response = requests.post(url, headers=self.headers, json=data)

        allure_response_logger(response)

        response.raise_for_status()
        return response.json()

    @allure.step("Get entity by ID {entity_id}")
    def get_entity(self, entity_id: int) -> Tuple[Dict[str, Any], int]:
        """Get entity by ID and return the data and status code."""
        url = f"{self.base_url}/api/get/{entity_id}"
        headers = {"accept": "application/json"}

        allure_request_logger("GET", url, headers)

        response = requests.get(url, headers=headers)

        allure_response_logger(response)

        return response.json(), response.status_code

    @allure.step("Get all entities")
    def get_all_entities(self) -> Tuple[Dict[str, Any], int]:
        """Get all entities and return the data and status code."""
        url = f"{self.base_url}/api/getAll"
        headers = {"accept": "application/json"}

        allure_request_logger("GET", url, headers)

        response = requests.get(url, headers=headers)

        allure_response_logger(response)

        return response.json(), response.status_code

    @allure.step("Update entity with ID {entity_id}")
    def update_entity(self, entity_id: int, data: Dict[str, Any]) -> int:
        """Update an entity and return the status code."""
        url = f"{self.base_url}/api/patch/{entity_id}"

        allure_request_logger("PATCH", url, self.headers, data)

        response = requests.patch(url, headers=self.headers, json=data)

        allure_response_logger(response)

        return response.status_code

    @allure.step("Delete entity with ID {entity_id}")
    def delete_entity(self, entity_id: int) -> int:
        """Delete an entity and return the status code."""
        url = f"{self.base_url}/api/delete/{entity_id}"
        headers = {"accept": "text/plain"}

        allure_request_logger("DELETE", url, headers)

        response = requests.delete(url, headers=headers)

        allure_response_logger(response)

        return response.status_code

    @staticmethod
    def remove_id_keys(d, expected_id=None, check_top_level_id=False):
        """Remove ID fields from the response for comparison."""
        result = {}
        for k, v in d.items():
            if k == "id":
                # Only check ID if both check_top_level_id is True AND expected_id is not None
                if check_top_level_id and expected_id is not None:
                    assert v == expected_id, f"Expected ID {expected_id}, but got {v}"
                continue

            if isinstance(v, dict):
                # Pass down the expected_id but don't check at deeper levels
                result[k] = EntityAPI.remove_id_keys(v, expected_id, False)
            elif isinstance(v, list):
                result[k] = [
                    EntityAPI.remove_id_keys(item, expected_id, False)
                    if isinstance(item, dict)
                    else item
                    for item in v
                ]
            else:
                result[k] = v

        return result
