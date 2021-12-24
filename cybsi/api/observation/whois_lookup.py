from uuid import UUID
from typing import Any, List, Optional, Dict
from .api import ObservationHeaderView
from ..internal import (
    BaseAPI,
    JsonObjectView,
)
from ..pagination import Page


class WhoisLookupObservationsAPI(BaseAPI):
    """Whois Lookup API."""

    _path = "/enrichment/observations/whois-lookups"

    def filter(
        self,
        entity_uuid: Optional[UUID] = None,
        data_source_uuids: Optional[List[UUID]] = None,
        reporter_uuids: Optional[List[UUID]] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page["WhoisLookupObservationView"]:
        """Get page of filtered whois lookups.

        Page's items are sorted in descending order of lookup time.

        Note:
            Calls `GET /enrichment/observations/whois-lookups`
        Args:
            entity_uuid: Entity identifier.
                Filter lookups of specified DomainName/IPAddress entity.
            data_source_uuids: List of data source identifiers.
                Filter lookups by original data source identifiers.
            reporter_uuids: List of reporter identifiers.
                Filter lookups by reporter data source identifiers.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of Whois lookups list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
        """
        params: Dict[str, Any] = {}

        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = str(limit)
        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if entity_uuid is not None:
            params["entityUUID"] = str(entity_uuid)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, WhoisLookupObservationView)
        return page

    def view(self, observation_uuid: UUID) -> "WhoisLookupObservationView":
        """Get the Whois lookup view.

        Note:
            Calls `GET /enrichment/observations/whois-lookups/{observation_uuid}`.
        Args:
            observation_uuid: Observation uuid.
        Returns:
            View of the observation.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Whois Lookup not found.
        """

        path = f"{self._path}/{observation_uuid}"
        r = self._connector.do_get(path)
        return WhoisLookupObservationView(r.json())


class WhoisLookupObservationView(ObservationHeaderView):
    """Whois Lookup view,
    as retrieved by :meth:`WhoisLookupObservationsAPI.view`."""

    @property
    def content(self) -> "WhoisLookupObservationContentView":
        """Content."""

        return WhoisLookupObservationContentView(self._get("content"))


class WhoisLookupObservationContentView(JsonObjectView):
    """Whois lookup content.

    TODO:
        Implement properties.
    """
