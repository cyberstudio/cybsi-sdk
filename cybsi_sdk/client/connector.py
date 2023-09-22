import requests

from typing import Callable
from urllib.parse import urljoin

from cybsi_sdk.exceptions import APIClientHTTPError, APIClientConnectorError
from cybsi_sdk.__version__ import __version__

requests.packages.urllib3.disable_warnings()


class HTTPConnector:

    def __init__(self, base_url: str,
                 auth: Callable = None,
                 ssl_verify=True):
        self._base_url = base_url
        self._auth = auth
        self._verify = ssl_verify
        self._headers = {
            'Accept': 'application/vnd.ptsecurity.app-v2',
            'User-Agent': f'cybsi-sdk-client/v{__version__}',
        }

    def _do(self, method: str, path: str, **kwargs):
        """Do HTTP request

        :param method: http method i.e GET, POST, PUT
        :param path: url path
        :param kwargs: any kwargs supported by request.Request
        """

        url = urljoin(self._base_url, path)
        kwargs.setdefault('headers', {}).update(**self._headers)

        req = requests.Request(method, url, auth=self._auth, **kwargs)
        s = requests.Session()

        try:
            resp = s.send(req.prepare(), verify=self._verify)
        except Exception as exp:
            raise APIClientConnectorError(exp) from None

        if not resp.ok:
            raise APIClientHTTPError(resp) from None

        return resp

    def do_get(self, path, params: dict = None, **kwargs) -> requests.Response:
        """Do http GET request

        :param path: url path
        :param params: query params
        :param kwargs: any kwargs which supported by requests library
        """

        return self._do('GET', path, params=params, **kwargs)

    def do_post(self, path, json=None, **kwargs) -> requests.Response:
        """Do http POST request

        :param path: url path
        :param json: json body
        :param kwargs: any kwargs which supported by requests library
        """

        return self._do('POST', path, json=json, **kwargs)
