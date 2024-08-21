from dataclasses import dataclass
from typing import Callable, Optional, Union

from .artifact import ArtifactsAPI, ArtifactsAsyncAPI
from .auth import APIKeyAuth, APIKeysAPI
from .client_config import DEFAULT_LIMITS, DEFAULT_TIMEOUTS, Limits, Timeouts
from .data_source import (
    DataSourcesAPI,
    DataSourcesAsyncAPI,
    DataSourceTypesAPI,
    DataSourceTypesAsyncAPI,
)
from .dictionary import DictionariesAPI, DictionariesAsyncAPI
from .enrichment import EnrichmentAPI, EnrichmentAsyncAPI
from .error import CybsiError
from .internal import HTTPConnector, JsonObjectView
from .internal.connector import AsyncHTTPConnector
from .license import LicensesAPI
from .observable import ObservableAPI, ObservableAsyncAPI
from .observation import ObservationsAPI, ObservationsAsyncAPI
from .replist import ReplistsAPI, ReplistsAsyncAPI
from .report import ReportsAPI, ReportsAsyncAPI
from .search import SearchAPI
from .search.api import SearchAsyncAPI
from .user import UsersAPI


@dataclass
class Config:
    """:class:`CybsiClient` config.

    Args:
        api_url: Base API URL.
        auth: Optional callable :class:`CybsiClient` can use to authenticate requests.
            In most cases it's enough to pass `api_key` instead of this.
        ssl_verify: Enable SSL certificate verification.
        timeouts: Timeout configuration. Default configuration is 60 sec
            on all operations.
        limits:  Configuration for limits to various client behaviors.
            Default configuration is max_connections=100, max_keepalive_connections=20.
        embed_object_url: Initialize URL property for all objects having uuid property
            (including :class:`~cybsi.api.view.RefView`).
            Views are compact if it's set to False.
    """

    api_url: str
    auth: Union[APIKeyAuth, Callable]
    ssl_verify: bool = True
    embed_object_url: bool = False
    timeouts: Timeouts = DEFAULT_TIMEOUTS
    limits: Limits = DEFAULT_LIMITS


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
        >>>
        >>> client.observations.generics.filter()
        >>> client.close()  # "with" syntax is also supported for CybsiClient
        <cybsi_sdk.client.observation.ObservationsAPI object at 0x7f57a293c190>
    """

    def __init__(self, config: Config):
        if config.auth is None:
            raise CybsiError("No authorization mechanism configured for client")

        self._connector = HTTPConnector(
            base_url=config.api_url,
            auth=config.auth,
            ssl_verify=config.ssl_verify,
            embed_object_url=config.embed_object_url,
            timeouts=config.timeouts,
            limits=config.limits,
        )

    def __enter__(self) -> "CybsiClient":
        self._connector.__enter__()
        return self

    def __exit__(
        self,
        exc_type=None,
        exc_value=None,
        traceback=None,
    ) -> None:
        self._connector.__exit__(exc_type, exc_value, traceback)

    def close(self) -> None:
        """Close client and release connections."""
        self._connector.close()

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
    def api_keys(self) -> APIKeysAPI:
        """API-Keys API handle."""
        return APIKeysAPI(self._connector)

    @property
    def dictionaries(self) -> DictionariesAPI:
        """Dictionaries API handle."""
        return DictionariesAPI(self._connector)

    @property
    def licenses(self) -> LicensesAPI:
        """Licenses API handle."""
        return LicensesAPI(self._connector)

    def version(self) -> "VersionView":
        """Get API and server version information.

        Note:
            Calls `GET /version`.
        Returns:
            Version view.
        """

        path = "/version"
        resp = self._connector.do_get(path)
        return VersionView(resp.json())


class CybsiAsyncClient:
    """The asynchronous analog of :class:`CybsiClient`.

    As you can see, the asynchronous client has fewer features than synchronous one.
    This is because we don't simply copy-paste features,
    but provide them only when they're actually useful in asynchronous applications.

    Args:
        config: Client config.
    """

    def __init__(self, config: Config):
        if config.auth is None:
            raise CybsiError("No authorization mechanism configured for client")

        self._connector = AsyncHTTPConnector(
            base_url=config.api_url,
            auth=config.auth,
            ssl_verify=config.ssl_verify,
            timeouts=config.timeouts,
            limits=config.limits,
        )

    async def __aenter__(self) -> "CybsiAsyncClient":
        await self._connector.__aenter__()
        return self

    async def __aexit__(
        self,
        exc_type=None,
        exc_value=None,
        traceback=None,
    ) -> None:
        await self._connector.__aexit__(exc_type, exc_value, traceback)

    async def aclose(self) -> None:
        """Close client and release connections."""
        await self._connector.aclose()

    @property
    def artifacts(self) -> ArtifactsAsyncAPI:
        """Artifacts API handle."""
        return ArtifactsAsyncAPI(self._connector)

    @property
    def enrichment(self) -> EnrichmentAsyncAPI:
        """Enrichment API handle."""
        return EnrichmentAsyncAPI(self._connector)

    @property
    def observations(self) -> ObservationsAsyncAPI:
        """Observations API handle."""
        return ObservationsAsyncAPI(self._connector)

    @property
    def reports(self) -> ReportsAsyncAPI:
        """Reports API handle."""
        return ReportsAsyncAPI(self._connector)

    @property
    def data_sources(self) -> DataSourcesAsyncAPI:
        """Data sources API handle."""
        return DataSourcesAsyncAPI(self._connector)

    @property
    def data_source_types(self) -> DataSourceTypesAsyncAPI:
        """Data source types API handle."""
        return DataSourceTypesAsyncAPI(self._connector)

    @property
    def replists(self) -> ReplistsAsyncAPI:
        """Replists API handle."""
        return ReplistsAsyncAPI(self._connector)

    @property
    def observable(self) -> ObservableAsyncAPI:
        """Observable API handle."""
        return ObservableAsyncAPI(self._connector)

    @property
    def search(self) -> SearchAsyncAPI:
        """Search API handle."""
        return SearchAsyncAPI(self._connector)

    @property
    def dictionaries(self) -> DictionariesAsyncAPI:
        """Dictionaries API handle."""
        return DictionariesAsyncAPI(self._connector)

    async def version(self) -> "VersionView":
        """Get API and server version information.

        Note:
            Calls `GET /version`.
        Returns:
            Version view.
        """

        path = "/version"
        resp = await self._connector.do_get(path)
        return VersionView(resp.json())


class VersionView(JsonObjectView):
    """Version view."""

    @property
    def api_version(self) -> "Version":
        """API specification version."""
        return Version(self._get("apiVersion"))

    @property
    def server_version(self) -> "Version":
        """Server version."""
        return Version(self._get("serverVersion"))


class Version:
    """Version."""

    def __init__(self, version: str):
        self._version = version

        p1, self._build = version.split("+", 1) if "+" in version else (version, "")
        core, self._prerelease = p1.split("-", 1) if "-" in p1 else (p1, "")
        self._major, self._minor, self._patch = [int(p) for p in core.split(".", 2)]

    def __str__(self):
        return self._version

    @property
    def major(self) -> int:
        """Major part of version."""

        return self._major

    @property
    def minor(self) -> int:
        """Minor part of version."""

        return self._minor

    @property
    def patch(self) -> int:
        """Patch part of version."""

        return self._patch

    @property
    def prerelease(self) -> Optional[str]:
        """Prerelease part of version."""

        if self._prerelease != "":
            return self._prerelease
        return None

    @property
    def build(self) -> Optional[str]:
        """Build part of version."""

        if self._build != "":
            return self._build
        return None
