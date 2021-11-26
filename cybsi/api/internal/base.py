"""
Base internal classes, useful to simplify API implementation.
"""

import json

from typing import Any, Callable, Dict, Optional

from ..error import CybsiError
from .connector import HTTPConnector


class BaseAPI:
    # Base class for all API handle implementations.
    def __init__(self, connector: HTTPConnector):
        self._connector = connector


class JsonObjectForm:
    def __init__(self):
        self._data = {}

    def __str__(self):
        return json.dumps(self._data, indent=2)

    def json(self):
        return self._data


class JsonObjectView:
    def __init__(self, data: Optional[Dict] = None):
        self._data = data or {}

    def __str__(self):
        return json.dumps(self._data, indent=2)

    def _get(self, key):
        try:
            return self._data[key]
        except KeyError as exp:
            msg = f"{self.__class__.__name__} does not have field: {exp}"
            raise CybsiError(msg) from None

    def _get_optional(self, key):
        return self._data.get(key, None)

    def _map_optional(self, key, mapper: Callable[[Any], Any]):
        value = self._get_optional(key)
        if value is not None:
            return mapper(value)
        return None

    def _map_list_optional(self, key, mapper: Callable[[Any], Any]):
        values = self._get_optional(key)
        if values is not None:
            return [mapper(val) for val in values]
        return None
