from requests import Response

from cybsi_sdk.error import CybsiError


class CybsiClientConnectionError(CybsiError):
    """Typically network error, can be retried.
    """
    pass


class CybsiClientHTTPError(CybsiError):
    """Unexpected API response status code, usually with status >= 400.

    TODO:
        Add property to get :class:`cybsi_sdk.client.common.ErrorView`?
    """
    def __init__(self, resp: Response):
        self.resp = resp
        super().__init__(f'unexpected http status code: {resp.status_code}')
