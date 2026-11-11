import unittest

from flask import json

from openapi_server.models.delete_response import DeleteResponse  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.plant_create_request import PlantCreateRequest  # noqa: E501
from openapi_server.models.plant_list_response import PlantListResponse  # noqa: E501
from openapi_server.models.plant_response import PlantResponse  # noqa: E501
from openapi_server.models.plant_update_request import PlantUpdateRequest  # noqa: E501
from openapi_server.test import BaseTestCase


class TestPlantsController(BaseTestCase):
    """PlantsController integration test stubs"""

    def test_plants_get(self):
        """Test case for plants_get

        Получить список растений
        """
        query_string = [('page', 1),
                        ('limit', 20)]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/plants',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_plants_plant_id_delete(self):
        """Test case for plants_plant_id_delete

        Удалить растение
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_plants_plant_id_get(self):
        """Test case for plants_plant_id_get

        Получить растение
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_plants_plant_id_patch(self):
        """Test case for plants_plant_id_patch

        Обновить данные растения
        """
        plant_update_request = {"name":"name","species":"species","wateringIntervalDays":5,"notes":"notes"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
            method='PATCH',
            headers=headers,
            data=json.dumps(plant_update_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_plants_post(self):
        """Test case for plants_post

        Создать растение
        """
        plant_create_request = {"name":"Монстера","species":"Monstera deliciosa","wateringIntervalDays":7,"notes":"Держать вдали от прямых солнечных лучей."}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/plants',
            method='POST',
            headers=headers,
            data=json.dumps(plant_create_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
