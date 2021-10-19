from dataclasses import dataclass
from typing import Callable

from .connector import HTTPConnector
from .observations import ObservationsAPI
from .replists import ReplistsAPI


@dataclass
class Config:
    api_url: str        # base client url
    auth: Callable      # callable object for making an authentication
    ssl_verify: bool    # enable ssl certificate verification


class CybsiClient:
    """Cybsi API low-level client
    """

    def __init__(self, config: Config):
        self._connector = HTTPConnector(
            base_url=config.api_url,
            auth=config.auth,
            ssl_verify=config.ssl_verify,
        )

    @property
    def observations(self):
        return ObservationsAPI(self._connector)

    @property
    def replists(self):
        return ReplistsAPI(self._connector)
