from typing import Any

import httpx

from cybsi.__version__ import __version__

from ..api import Tag
from ..error import CybsiError, _raise_for_status

_IF_MATCH_HEADER = "If-Match"

_BASIC_HEADERS = {
    "Accept": "application/vnd.ptsecurity.app-v2",
    "User-Agent": f"cybsi-sdk-client/v{__version__}",
}


class HTTPConnector:
    """Connector performing round trips to Cybsi."""

    def __init__(self, base_url: str, auth: Any, ssl_verify=True):
        self._client = httpx.Client(
            auth=auth, verify=ssl_verify, base_url=base_url, headers=_BASIC_HEADERS
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

    def do_get(
        self, path, params: dict = None, stream=False, **kwargs
    ) -> httpx.Response:
        return self._do("GET", path, params=params, stream=stream, **kwargs)

    def do_post(self, path, json=None, **kwargs) -> httpx.Response:
        return self._do("POST", path, json=json, **kwargs)

    def do_patch(self, path, tag: Tag, json=None, **kwargs) -> httpx.Response:
        headers = kwargs.setdefault("headers", {})
        headers[_IF_MATCH_HEADER] = tag
        return self._do("PATCH", path, json=json, **kwargs)

    def do_put(self, path, json=None, **kwargs) -> httpx.Response:
        return self._do("PUT", path, json=json, **kwargs)

    def do_delete(self, path, params: dict = None, **kwargs) -> httpx.Response:
        return self._do("DELETE", path, params=params, **kwargs)

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


class AsyncHTTPConnector:
    """Asynchronous connector performing round trips to Cybsi."""

    def __init__(self, base_url: str, auth: Any, ssl_verify=True):
        limits = httpx.Limits(max_keepalive_connections=1, max_connections=1)
        self._client = httpx.AsyncClient(
            auth=auth,
            verify=ssl_verify,
            base_url=base_url,
            headers=_BASIC_HEADERS,
            limits=limits,
        )

    async def __aenter__(self) -> "AsyncHTTPConnector":
        await self._client.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type=None,
        exc_value=None,
        traceback=None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_value, traceback)

    async def aclose(self) -> None:
        """Close client and release connections."""
        await self._client.aclose()

    async def do_get(
        self, path, params: dict = None, stream=False, **kwargs
    ) -> httpx.Response:
        return await self._do("GET", path, params=params, stream=stream, **kwargs)

    async def do_post(self, path, json=None, **kwargs) -> httpx.Response:
        return await self._do("POST", path, json=json, **kwargs)

    async def do_patch(self, path, tag: Tag, json=None, **kwargs) -> httpx.Response:
        headers = kwargs.setdefault("headers", {})
        headers[_IF_MATCH_HEADER] = tag
        return await self._do("PATCH", path, json=json, **kwargs)

    async def do_put(self, path, json=None, **kwargs) -> httpx.Response:
        return await self._do("PUT", path, json=json, **kwargs)

    async def do_delete(self, path, params: dict = None, **kwargs) -> httpx.Response:
        return await self._do("DELETE", path, params=params, **kwargs)

    async def _do(self, method: str, path: str, stream=False, **kwargs):
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
            resp = await self._client.send(request=req, stream=stream)
        except CybsiError:
            raise
        except Exception as exp:
            raise CybsiError("could not send request", exp) from exp

        _raise_for_status(resp)

        return resp
