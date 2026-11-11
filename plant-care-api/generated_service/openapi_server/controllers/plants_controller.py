import flask
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.delete_response import DeleteResponse  # noqa: E501
from openapi_server.models.error_response import ErrorResponse  # noqa: E501
from openapi_server.models.plant_create_request import PlantCreateRequest  # noqa: E501
from openapi_server.models.plant_list_response import PlantListResponse  # noqa: E501
from openapi_server.models.plant_response import PlantResponse  # noqa: E501
from openapi_server.models.plant_update_request import PlantUpdateRequest  # noqa: E501
from openapi_server import util


def plants_get(page=None, limit=None):  # noqa: E501
    """Получить список растений

    Возвращает постраничный список растений, принадлежащих аутентифицированному пользователю. # noqa: E501

    :param page: Номер страницы, начиная с 1.
    :type page: int
    :param limit: Количество растений на странице.
    :type limit: int

    :rtype: Union[PlantListResponse, Tuple[PlantListResponse, int], Tuple[PlantListResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def plants_plant_id_delete(plant_id):  # noqa: E501
    """Удалить растение

    Удаляет растение, принадлежащее аутентифицированному пользователю. # noqa: E501

    :param plant_id: Публичный идентификатор растения.
    :type plant_id: str
    :type plant_id: str

    :rtype: Union[DeleteResponse, Tuple[DeleteResponse, int], Tuple[DeleteResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def plants_plant_id_get(plant_id):  # noqa: E501
    """Получить растение

    Возвращает одно растение, принадлежащее аутентифицированному пользователю. # noqa: E501

    :param plant_id: Публичный идентификатор растения.
    :type plant_id: str
    :type plant_id: str

    :rtype: Union[PlantResponse, Tuple[PlantResponse, int], Tuple[PlantResponse, int, Dict[str, str]]
    """
    return 'do some magic!'


def plants_plant_id_patch(plant_id, body):  # noqa: E501
    """Обновить данные растения

    Частично обновляет доступные для изменения данные растения. # noqa: E501

    :param plant_id: Публичный идентификатор растения.
    :type plant_id: str
    :type plant_id: str
    :param plant_update_request: 
    :type plant_update_request: dict | bytes

    :rtype: Union[PlantResponse, Tuple[PlantResponse, int], Tuple[PlantResponse, int, Dict[str, str]]
    """
    plant_update_request = body
    if flask.request.is_json:
        plant_update_request = PlantUpdateRequest.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'


def plants_post(body):  # noqa: E501
    """Создать растение

    Создаёт новое растение для аутентифицированного пользователя. # noqa: E501

    :param plant_create_request: 
    :type plant_create_request: dict | bytes

    :rtype: Union[PlantResponse, Tuple[PlantResponse, int], Tuple[PlantResponse, int, Dict[str, str]]
    """
    plant_create_request = body
    if flask.request.is_json:
        plant_create_request = PlantCreateRequest.from_dict(flask.request.get_json())  # noqa: E501
    return 'do some magic!'
