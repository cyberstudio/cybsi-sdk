import requests

from typing import Callable
from urllib.parse import urljoin

from cybsi.__version__ import __version__

from ..error import CybsiClientConnectionError, CybsiClientHTTPError

requests.packages.urllib3.disable_warnings()


class HTTPConnector:
    """Connector performing round trips to Cybsi."""
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
        """Do HTTP request.

        Args:
            method: HTTP method i.e GET, POST, PUT.
            path: URL path.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        Raise:
            :class:`CybsiAPIClientConnectorError` on network errors
            :class:`CybsiAPIClientHTTPError` if response status code is >= 400
        """

        url = urljoin(self._base_url, path)
        kwargs.setdefault('headers', {}).update(**self._headers)

        req = requests.Request(method, url, auth=self._auth, **kwargs)
        s = requests.Session()

        try:
            resp = s.send(req.prepare(), verify=self._verify)
        except Exception as exp:
            raise CybsiClientConnectionError(exp) from None

        if not resp.ok:
            raise CybsiClientHTTPError(resp) from None

        return resp

    def do_get(self, path, params: dict = None, **kwargs) -> requests.Response:
        """Do HTTP GET request.

        Args:
            path: URL path.
            params: Query params.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        """
        return self._do('GET', path, params=params, **kwargs)

    def do_post(self, path, json=None, **kwargs) -> requests.Response:
        """Do HTTP POST request.

        Args:
            path: URL path.
            json: JSON body.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        """
        return self._do('POST', path, json=json, **kwargs)
