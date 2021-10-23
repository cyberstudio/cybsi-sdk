import unittest
import requests
import json

from unittest.mock import patch

from cybsi_sdk.client.connector import HTTPConnector
from cybsi_sdk.__version__ import __version__


class HTTPConnectorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.base_url = "http://localhost"
        self.connector = HTTPConnector(base_url=self.base_url, auth=None)

    @patch.object(requests.Session, 'send')
    def test_connector_default_headers(self, mock):
        self.connector.do_get('/test')

        args, _ = mock.call_args
        req: requests.PreparedRequest = args[0]

        self.assertEqual(
            'application/vnd.ptsecurity.app-v2', req.headers.get('Accept')
        )
        self.assertEqual(
            f'cybsi-sdk-client/v{__version__}', req.headers.get('User-Agent')
        )

    @patch.object(requests.Session, 'send')
    def test_connector_default_ssl_verify(self, mock):
        connector = HTTPConnector(base_url=self.base_url, auth=None)
        connector.do_get('test')
        _, kwargs = mock.call_args
        self.assertTrue(kwargs.get('verify'))

    @patch.object(requests.Session, 'send')
    def test_connector_set_ssl_verify(self, mock):
        connector = HTTPConnector(base_url=self.base_url, ssl_verify=False)
        connector.do_get('test')
        _, kwargs = mock.call_args
        self.assertFalse(kwargs.get('verify'))

    @patch.object(requests.Session, 'send')
    def test_connector_do_get(self, mock):
        status_code = 200
        mock.return_value.status_code = status_code

        self.connector.do_get('/test', params={'p1': 'v1'})
        args, _ = mock.call_args
        req: requests.PreparedRequest = args[0]

        self.assertEqual('GET', req.method)
        self.assertEqual(f'{self.base_url}/test?p1=v1', req.url)

    @patch.object(requests.Session, 'send')
    def test_connector_do_post(self, mock):
        status_code = 200
        mock.return_value.status_code = status_code
        body = {'field1': 'value1', 'field2': 'value2'}
        self.connector.do_post('/test', json=body)

        args, _ = mock.call_args
        req: requests.PreparedRequest = args[0]

        self.assertEqual('POST', req.method)
        self.assertEqual(f'{self.base_url}/test', req.url)
        self.assertEqual(body, json.loads(req.body))