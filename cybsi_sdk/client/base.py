import json
import requests
from .connector import HTTPConnector


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


class ResponseView:

    def __init__(self, resp: requests.Response):
        self._resp = resp
        self._data = resp.json()

    def __str__(self):
        return json.dumps(self._data, indent=2)


class RefView(ResponseView):

    @property
    def uuid(self):
        """Get uuid
        """
        return self._data.get("uuid")

    @property
    def url(self):
        """Get url
        """
        return self._data.get("url")
