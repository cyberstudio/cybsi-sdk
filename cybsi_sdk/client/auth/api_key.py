import logging
import requests

from typing import Optional

from ..error import CybsiClientConnectionError
from ..internal import HTTPConnector
from .token import TokenView

logger = logging.getLogger(__name__)


class APIKeyAuth:
    """Callable. Authomatically handles authentication
    of :class:`CybsiClient` requests using API key.

    Args:
        api_url: Cybsi API URL.
        api_key: Cybsi API key.
        ssl_verify: enable SSL verification.
    Usage:
        >>> from cybsi_sdk.client import APIKeyAuth, Config, CybsiClient
        >>> api_url = "http://localhost:80/api"
        >>> api_key = "8Nqjk6V4Q_et_Rf5EPu4SeWy4nKbVPKPzKJESYdRd7E"
        >>> auth = APIKeyAuth(api_url, api_key)
        >>> config = Config(api_url, auth)
        >>> client = CybsiClient(config)
        >>> client.observations
        <cybsi_sdk.client.observation.ObservationsAPI object at 0x7f57a293c190>
    """
    _get_token_path = 'auth/token'

    def __init__(self, api_url: str, api_key: str, ssl_verify: bool = True):
        self._api_key = api_key
        self._connector = HTTPConnector(api_url, ssl_verify=ssl_verify)
        self._token = None  # type: Optional[str]

    def __call__(self, r: requests.Request):
        # Get access token from Cybsi using API key and retry HTTP
        # request if 401 response is received.
        if self._token:
            r.headers['Authorization'] = self._token

        r.register_hook('response', self._handle_401)
        return r

    def _handle_401(self, r, **kwargs):
        """Handler for 401 http response
        """

        if r.status_code != 401:
            return r

        r.close()
        req = r.request.copy()

        logger.debug('request: %s %s, unauthorized.', req.method, req.url)

        resp = self._connector.do_get(
            self._get_token_path,
            params={'apiKey': self._api_key}
        )
        token = TokenView(resp.json())

        self._token = f'{token.type} {token.access_token}'
        req.headers['Authorization'] = self._token

        try:
            _r = r.connection.send(req, **kwargs)
        except Exception as exp:
            raise CybsiClientConnectionError(
                f'unable to send authenticated request: {exp}'
            ) from None

        _r.history.append(r)
        _r.request = req
        return _r
