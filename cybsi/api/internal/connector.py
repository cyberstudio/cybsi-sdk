import requests

from typing import Callable
from urllib.parse import urljoin

from cybsi.__version__ import __version__

from ..error import (
    CybsiError,
    InvalidRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    ResourceModifiedError,
    SemanticError,
)

requests.packages.urllib3.disable_warnings()


class HTTPConnector:
    """Connector performing round trips to Cybsi."""

    def __init__(self, base_url: str, auth: Callable = None, ssl_verify=True):
        self._base_url = base_url
        self._auth = auth
        self._verify = ssl_verify
        self._headers = {
            "Accept": "application/vnd.ptsecurity.app-v2",
            "User-Agent": f"cybsi-sdk-client/v{__version__}",
        }
        self._error_mapping = {
            400: InvalidRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
            409: ConflictError,
            412: ResourceModifiedError,
            422: SemanticError,
        }

    def _do(self, method: str, path: str, stream=False, **kwargs):
        """Do HTTP request.

        Args:
            method: HTTP method i.e GET, POST, PUT.
            path: URL path.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        Raise:
            :class:`~cybsi.api.error.CybsiError`: On connectivity issues.
            :class:`~cybsi.api.error.APIError`: If response status code is >= 400
        """

        url = urljoin(self._base_url, path)
        kwargs.setdefault("headers", {}).update(**self._headers)

        req = requests.Request(method, url, auth=self._auth, **kwargs)
        s = requests.Session()

        try:
            resp = s.send(req.prepare(), verify=self._verify, stream=stream)
        except Exception as exp:
            raise CybsiError("could not send request", exp) from None

        self._raise_for_status(resp)

        return resp

    def do_get(
        self, path, params: dict = None, stream=False, **kwargs
    ) -> requests.Response:
        """Do HTTP GET request.

        Args:
            path: URL path.
            params: Query params.
            stream: Stream response.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        """
        return self._do("GET", path, params=params, stream=stream, **kwargs)

    def do_post(self, path, json=None, **kwargs) -> requests.Response:
        """Do HTTP POST request.

        Args:
            path: URL path.
            json: JSON body.
            kwargs: Any kwargs supported by request.Request.
        Return:
            Response.
        """
        return self._do("POST", path, json=json, **kwargs)

    def _raise_for_status(self, resp: requests.Response) -> None:
        if resp.ok:
            return

        err_cls = self._error_mapping.get(resp.status_code, None)
        if err_cls is not None:
            raise err_cls(resp.json())

        raise CybsiError(
            f"unexpected response status code: {resp.status_code}. "
            f"Request body: {resp.text}"
        )
