from typing import Any

import httpx

from cybsi.__version__ import __version__

from ..api import Tag
from ..error import CybsiError, _raise_for_status


class HTTPConnector:
    """Connector performing round trips to Cybsi."""

    _if_match_header = "If-Match"

    def __init__(self, base_url: str, auth: Any, ssl_verify=True):
        headers = {
            "Accept": "application/vnd.ptsecurity.app-v2",
            "User-Agent": f"cybsi-sdk-client/v{__version__}",
        }

        self._client = httpx.Client(
            auth=auth, verify=ssl_verify, base_url=base_url, headers=headers
        )

    def __enter__(self) -> "HTTPConnector":
        self._client.__enter__()
        return self

    def __exit__(
        self,
        exc_type=None,
        exc_value=None,
        traceback=None,
    ) -> None:
        self._client.__exit__(exc_type, exc_value, traceback)

    def close(self) -> None:
        """Close client and release connections."""
        self._client.close()

    def _do(self, method: str, path: str, stream=False, **kwargs):
        """Do HTTP request.

        Args:
            method: HTTP method i.e GET, POST, PUT.
            path: URL path.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        Raise:
            :class:`~cybsi.api.error.CybsiError`: On connectivity issues.
            :class:`~cybsi.api.error.APIError`: If response status code is >= 400
        """
        req = self._client.build_request(method, url=path, **kwargs)
        try:
            resp = self._client.send(request=req, stream=stream)
        except CybsiError:
            raise
        except Exception as exp:
            raise CybsiError("could not send request", exp) from exp

        _raise_for_status(resp)

        return resp

    def do_get(
        self, path, params: dict = None, stream=False, **kwargs
    ) -> httpx.Response:
        """Do HTTP GET request.

        Args:
            path: URL path.
            params: Query params.
            stream: Stream response.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        """
        return self._do("GET", path, params=params, stream=stream, **kwargs)

    def do_post(self, path, json=None, **kwargs) -> httpx.Response:
        """Do HTTP POST request.

        Args:
            path: URL path.
            json: JSON body.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        """
        return self._do("POST", path, json=json, **kwargs)

    def do_patch(self, path, tag: Tag, json=None, **kwargs) -> httpx.Response:
        """Do HTTP PATCH request.

        Args:
            path: URL path.
            tag: ETag value.
            json: JSON body.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        """
        headers = kwargs.setdefault("headers", {})
        headers[self._if_match_header] = tag
        return self._do("PATCH", path, json=json, **kwargs)

    def do_put(self, path, json=None, **kwargs) -> httpx.Response:
        """Do HTTP PUT request.

        Args:
            path: URL path.
            json: JSON body.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        """
        return self._do("PUT", path, json=json, **kwargs)

    def do_delete(self, path, params: dict = None, **kwargs) -> httpx.Response:
        """Do HTTP PUT request.

        Args:
            path: URL path.
            params: Query params.
            kwargs: Any kwargs supported by httpx.Request.
        Return:
            Response.
        """
        return self._do("DELETE", path, params=params, **kwargs)
