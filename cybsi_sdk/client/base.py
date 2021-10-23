"""
Base internal classes, useful to simplify API implementation.
"""

import json

from typing import Dict, Optional, List

from .connector import HTTPConnector

from cybsi_sdk.exceptions import CybsiInvalidViewData


class API:
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
            msg = f'{self.__class__.__name__} does not have field: {exp}'
            raise CybsiInvalidViewData(msg) from None


class JsonListView:

    def __init__(self, data: Optional[List] = None):
        self._data = data or []

    def __str__(self):
        return json.dumps(self._data, indent=2)


class RefView(JsonObjectView):

    @property
    def uuid(self):
        """Get uuid
        FIXME: return uuid, not string
        """
        return self._get("uuid")

    @property
    def url(self):
        """Get url
        """
        return self._get("url")
