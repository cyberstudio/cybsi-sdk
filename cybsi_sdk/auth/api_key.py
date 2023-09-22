import logging
import requests

from cybsi_sdk.client import auth
from cybsi_sdk.client.connector import HTTPConnector
from cybsi_sdk.exceptions import APIClientException

logger = logging.getLogger(__name__)


class APIKeyAuth:
    """APIKeyAuth implements cybsi client api key authentication.

    It gets access token from cybsi using api-key and retries http
    request if 401 response is received.
    """
    _get_token_path = 'auth/token'

    def __init__(self, api_url: str, api_key: str, ssl_verify: bool = True):
        """APIKeyAuth initializer

        :param api_url: cybsi auth client url
        :param api_key: cybsi client key
        :param ssl_verify: enable ssl verification
        """

        self._api_key = api_key
        self._connector = HTTPConnector(api_url, ssl_verify=ssl_verify)
        self._token = None

    def __call__(self, r: requests.Request):
        if self._token:
            r.headers['Authorization'] = self._token

        r.register_hook('response', self.handle_401)
        return r

    def handle_401(self, r: requests.Response, **kwargs):
        """Handler for 401 http response
        """

        if r.status_code != 401:
            return r

        r.close()
        req = r.request.copy()

        logger.debug('request: %s %s, unauthorized.', req.method, req.url)

        try:
            resp = self._connector.do_get(
                self._get_token_path,
                params={'apiKey': self._api_key}
            )
            resp.raise_for_status()
        except Exception as exp:
            raise APIClientException(
                f'unable to get access token: {exp}'
            ) from None

        token = auth.TokenView(resp)

        self._token = f'{token.type} {token.access_token}'
        req.headers['Authorization'] = self._token

        try:
            _r = r.connection.send(req, **kwargs)
        except Exception as exp:
            raise APIClientException(
                f'unable to send authenticated request: {exp}'
            ) from None

        _r.history.append(r)
        _r.request = req
        return _r
