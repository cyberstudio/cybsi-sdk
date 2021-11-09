from requests import Response


class CybsiError(Exception):
    """Base exception used by SDK."""
    pass


class CybsiClientConnectionError(CybsiError):
    """Typically network error, can be retried.
    """
    pass


class CybsiClientHTTPError(CybsiError):
    """Unexpected API response status code, usually with status >= 400.

    TODO:
        Add property to get :class:`cybsi.api.common.ErrorView`?
    """
    def __init__(self, resp: Response):
        self.resp = resp
        super().__init__(f'unexpected http response: {resp.status_code}, '
                         f'{resp.text}')
