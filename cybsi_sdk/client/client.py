from dataclasses import dataclass
from typing import Callable

from .internal import HTTPConnector
from .observation.api import ObservationsAPI
from .replist.api import ReplistsAPI


@dataclass
class Config:
    """:class:`CybsiClient` config."""
    api_url: str  #: Base API URL.
    auth: Callable  # noqa: E501 #: Callable object :class:`CybsiClient` can use to authenticate requests.
    ssl_verify: bool = True  #: Enable SSL certificate verification.


class CybsiClient:
    """The main entry point for all actions with Cybsi REST API.

    As the client is low-level, it is structured around Cybsi REST API routes.
    Use properties of the client to retrieve handles of API sections.

    The client also follows Cybsi REST API input-output formats,
    providing little to no abstration from JSONs API uses.
    It's relatively easy to construct an invalid request,
    so use client's functions wisely.

    Args:
        config: Client config.
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

    def __init__(self, config: Config):
        self._connector = HTTPConnector(
            base_url=config.api_url,
            auth=config.auth,
            ssl_verify=config.ssl_verify,
        )

    @property
    def observations(self) -> ObservationsAPI:
        """Observations API handle."""
        return ObservationsAPI(self._connector)

    @property
    def replists(self) -> ReplistsAPI:
        """Reputation lists API handle."""
        return ReplistsAPI(self._connector)
