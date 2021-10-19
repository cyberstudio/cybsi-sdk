from requests import Response


class CybsiException(Exception):
    pass


class CybsiInvalidViewData(CybsiException):
    pass


class APIClientException(CybsiException):
    pass


class APIClientConnectorError(APIClientException):
    pass


class APIClientHTTPError(APIClientException):
    def __init__(self, resp: Response):
        self.resp = resp
        super().__init__(f'unexpected http status code: {resp.status_code}')
