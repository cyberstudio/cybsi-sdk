"""A set of exceptions SDK and API client can raise.
"""
from requests import Response


class CybsiException(Exception):
    """Base exception used by SDK"""
    pass


class CybsiInvalidViewData(CybsiException):
    """Received invalid response content from API.
    TODO: Move or rename, make this exception private for SDK.
    """
    pass


class APIClientException(CybsiException):
    """Network error
    TODO: Document when to expect, maybe move.
    """
    pass


class APIClientConnectorError(APIClientException):
    """Network error?
    TODO: Document the difference with APIClientException or remove.
    """
    pass


class APIClientHTTPError(APIClientException):
    """Unexpected responce status code
    TODO: Maybe merge with CybsiInvalidViewData?
    """
    def __init__(self, resp: Response):
        self.resp = resp
        super().__init__(f'unexpected http status code: {resp.status_code}')
