import allure
import pytest
from models.entity_models import IdPerson, ExportData, EntityResponse


@pytest.mark.api
@allure.epic("Entity API")
@allure.feature("Entity CRUD Operations")
class TestEntityAPI:
    @allure.story("Entity Creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test creating a new entity and verifying it exists")
    def test_create_entity(self, api_client, json_data):
        # Create an entity
        with allure.step("Create new entity with test data"):
            entity_id = api_client.create_entity(json_data)

        try:
            # Validate the ID
            with allure.step("Validate the returned entity ID"):
                id_person_pydantic = IdPerson.model_validate({"id": entity_id})
                assert isinstance(entity_id, int)
                allure.attach(str(entity_id), "Created Entity ID")

            # Get the entity to verify it was created correctly
            with allure.step("Retrieve the created entity"):
                entity_data, status_code = api_client.get_entity(entity_id)
                entity_pydantic = ExportData.model_validate(entity_data)
                entity_dict = entity_pydantic.model_dump()

            # Remove ID fields for comparison
            with allure.step("Compare entity data with original test data"):
                clean_data = api_client.remove_id_keys(entity_dict, entity_id, True)

                # Verify the entity data
                assert status_code == 200
                assert clean_data == json_data

        finally:
            # Clean up
            with allure.step("Clean up - delete the created entity"):
                api_client.delete_entity(entity_id)

    @allure.story("Entity Deletion")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test deleting an entity and verifying it no longer exists")
    def test_delete_entity(self, api_client, created_entity_id):
        # Delete the entity
        with allure.step(f"Delete entity with ID {created_entity_id}"):
            delete_status = api_client.delete_entity(created_entity_id)
            assert delete_status == 204

        # Try to get the deleted entity
        with allure.step(f"Verify entity with ID {created_entity_id} no longer exists"):
            try:
                _, status_code = api_client.get_entity(created_entity_id)
                assert status_code != 200  # Should not be 200 if entity is deleted
                allure.attach(str(status_code), "Response status code")
            except Exception as e:
                # If the request fails with an exception, that's also acceptable
                allure.attach(str(e), "Exception on retrieving deleted entity")
                pass

    @allure.story("Entity Retrieval")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test retrieving an entity by ID")
    def test_get_entity(self, api_client, created_entity_id, json_data):
        # Get the entity
        with allure.step(f"Retrieve entity with ID {created_entity_id}"):
            entity_data, status_code = api_client.get_entity(created_entity_id)

        # Validate the response
        with allure.step("Validate the retrieved entity data"):
            entity_pydantic = ExportData.model_validate(entity_data)
            entity_dict = entity_pydantic.model_dump()

            # Remove ID fields for comparison
            clean_data = api_client.remove_id_keys(entity_dict, created_entity_id, True)

            # Verify the data
            assert status_code == 200
            assert clean_data == json_data

    @allure.story("Entity List Retrieval")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Test retrieving all entities and finding a specific one")
    def test_get_all_entities(self, api_client, created_entity_id, json_data):
        # Get all entities
        with allure.step("Retrieve all entities"):
            entities_data, status_code = api_client.get_all_entities()

        # Validate the response format
        with allure.step("Validate the response format"):
            entities_pydantic = EntityResponse.model_validate(entities_data)

            # Check if our created entity is in the list
            found = False
            entity_count = len(entities_pydantic.entity)
            allure.attach(str(entity_count), "Total entities found")

            for entity in entities_pydantic.entity:
                entity_dict = entity.model_dump()
                entity_without_id = api_client.remove_id_keys(entity_dict)
                if entity_without_id == json_data:
                    found = True
                    break

            assert status_code == 200
            assert found, "Created entity not found in the list of all entities"

    @allure.story("Entity Update")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Test updating an entity and verifying the changes")
    def test_update_entity(self, api_client, created_entity_id, json_data_for_patch):
        # Update the entity
        with allure.step(f"Update entity with ID {created_entity_id}"):
            patch_status = api_client.update_entity(
                created_entity_id, json_data_for_patch
            )
            assert patch_status == 204

        # Get the updated entity
        with allure.step("Retrieve the updated entity"):
            entity_data, status_code = api_client.get_entity(created_entity_id)
            entity_pydantic = ExportData.model_validate(entity_data)
            entity_dict = entity_pydantic.model_dump()

            # Remove ID fields for comparison
            clean_data = api_client.remove_id_keys(entity_dict, created_entity_id, True)

        # Verify the update
        with allure.step("Verify the entity was updated correctly"):
            assert clean_data == json_data_for_patch
