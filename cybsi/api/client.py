from dataclasses import dataclass
from typing import Callable

from .artifact import ArtifactsAPI
from .data_source import DataSourcesAPI, DataSourceTypesAPI
from .enrichment import EnrichmentAPI
from .internal import HTTPConnector
from .observable import ObservableAPI
from .observation import ObservationsAPI
from .replist import ReplistsAPI
from .report import ReportsAPI
from .search import SearchAPI
from .user import UsersAPI
from .api_keys import APIKeys


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

    Hint:
        Use :class:`~cybsi.api.CybsiClient` properties
        to construct needed API handles. Don't construct sub-APIs manually.

        Do this:
            >>> from cybsi.api import CybsiClient
            >>> client = CybsiClient(config)
            >>> client.observations.generics.view(observation_uuid)
        Not this:
            >>> from cybsi.api.observation import GenericObservationsAPI
            >>> GenericObservationsAPI(connector).view(observation_uuid)

    Args:
        config: Client config.
    Usage:
        >>> from cybsi.api import APIKeyAuth, Config, CybsiClient
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
    def artifacts(self) -> ArtifactsAPI:
        """Artifacts API handle."""
        return ArtifactsAPI(self._connector)

    @property
    def data_sources(self) -> DataSourcesAPI:
        """Data sources API handle."""
        return DataSourcesAPI(self._connector)

    @property
    def data_source_types(self) -> DataSourceTypesAPI:
        """Data source types API handle."""
        return DataSourceTypesAPI(self._connector)

    @property
    def enrichment(self) -> EnrichmentAPI:
        """Enrichment API handle."""
        return EnrichmentAPI(self._connector)

    @property
    def observable(self) -> ObservableAPI:
        """Observable API handle."""
        return ObservableAPI(self._connector)

    @property
    def observations(self) -> ObservationsAPI:
        """Observations API handle."""
        return ObservationsAPI(self._connector)

    @property
    def replists(self) -> ReplistsAPI:
        """Reputation lists API handle."""
        return ReplistsAPI(self._connector)

    @property
    def reports(self) -> ReportsAPI:
        """Reports API handle."""
        return ReportsAPI(self._connector)

    @property
    def search(self) -> SearchAPI:
        """Search API handle."""
        return SearchAPI(self._connector)

    @property
    def users(self) -> UsersAPI:
        """Users API handle."""
        return UsersAPI(self._connector)

    @property
    def api_keys(self) -> APIKeys:
        """API-Keys API handle."""
        return APIKeys(self._connector)
