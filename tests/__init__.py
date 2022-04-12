import unittest
import requests
import datetime
import json
from cybsi.api.internal import parse_rfc3339_timestamp
from typing import Union


class BaseTest(unittest.TestCase):
    @staticmethod
    def _make_response(status_code: int, content: Union[list, dict]):
        """Make mock response"""
        resp = requests.Response()
        resp.status_code = status_code
        resp._content = json.dumps(content, indent=2).encode("utf-8")
        return resp

    @staticmethod
    def assert_timestamp(expected_timestamp: str, actual_timestamp: datetime.datetime):
        """Assert given timestamp with expected

        expected_timestamp string format is %Y-%m-%dT%H:%M:%S.%fZ
        """
        assert parse_rfc3339_timestamp(expected_timestamp) == actual_timestamp
