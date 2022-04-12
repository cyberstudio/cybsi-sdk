import json
import unittest
from unittest.mock import patch

import httpx

from cybsi.__version__ import __version__
from cybsi.api.error import CybsiError, NotFoundError
from cybsi.api.internal.connector import HTTPConnector


class HTTPConnectorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = "http://localhost"
        self.connector = HTTPConnector(base_url=self.base_url, auth=None)

    @patch.object(httpx.Client, "send")
    def test_connector_default_headers(self, mock):
        mock.return_value.status_code = 200

        self.connector.do_get("/test")
        _, kwargs = mock.call_args
        req: httpx.Request = kwargs["request"]

        self.assertEqual("application/vnd.ptsecurity.app-v2", req.headers.get("Accept"))
        self.assertEqual(
            f"cybsi-sdk-client/v{__version__}", req.headers.get("User-Agent")
        )

    @patch.object(httpx.Client, "send")
    def test_connector_do_get(self, mock):
        status_code = 200
        mock.return_value.status_code = status_code

        self.connector.do_get("/test", params={"p1": "v1"})
        _, kwargs = mock.call_args
        req: httpx.Request = kwargs["request"]

        self.assertEqual("GET", req.method)
        self.assertEqual(f"{self.base_url}/test?p1=v1", req.url)

    @patch.object(httpx.Client, "send")
    def test_connector_do_post(self, mock):
        status_code = 200
        mock.return_value.status_code = status_code
        body = {"field1": "value1", "field2": "value2"}
        self.connector.do_post("/test", json=body)

        _, kwargs = mock.call_args
        req: httpx.Request = kwargs["request"]

        self.assertEqual("POST", req.method)
        self.assertEqual(f"{self.base_url}/test", req.url)
        self.assertEqual(body, json.loads(req.content))

    @patch.object(httpx.Client, "send")
    def test_connector_do_post_503(self, mock):
        mock.return_value = self._make_response(
            503, b"Server is busy laying on the floor"
        )

        with self.assertRaises(CybsiError):
            self.connector.do_post("/test", json={})

    @patch.object(httpx.Client, "send")
    def test_connector_do_get_404(self, mock):
        mock.return_value = self._make_response(404, b'{"code": "NotFound"}')

        with self.assertRaises(NotFoundError):
            self.connector.do_get("/test")

    @staticmethod
    def _make_response(status_code, content):
        return httpx.Response(status_code=status_code, content=content)
