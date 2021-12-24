from uuid import UUID
from typing import Any, List, Optional, Dict
from .api import ObservationHeaderView
from ..internal import (
    BaseAPI,
    JsonObjectView,
)
from ..pagination import Page


class ThreatObservationsAPI(BaseAPI):
    """Threat observation API."""

    _path = "/enrichment/observations/threats"

    def filter(
        self,
        entity_uuid: Optional[UUID] = None,
        data_source_uuids: Optional[List[UUID]] = None,
        reporter_uuids: Optional[List[UUID]] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page["ThreatObservationView"]:
        """Get page of filtered observations.

        Page's items are sorted in descending order of observation time.

        Note:
            Calls `GET /enrichment/observations/threats`
        Args:
            entity_uuid: Entity identifier.
                Filter threats of specified file entity.
            data_source_uuids: List of data source identifiers.
                Filter observation by original data source identifiers.
            reporter_uuids: List of reporter identifiers.
                Filter observation by reporter data source identifiers.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of observation list and next page cursor.
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
        page = Page(self._connector.do_get, resp, ThreatObservationView)
        return page

    def view(self, observation_uuid: UUID) -> "ThreatObservationView":
        """Get the Threat observation view.

        Note:
            Calls `GET /enrichment/observations/threats/{observation_uuid}`.
        Args:
            observation_uuid: Observation uuid.
        Returns:
            View of the observation.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: observation not found.
        """

        path = f"{self._path}/{observation_uuid}"
        r = self._connector.do_get(path)
        return ThreatObservationView(r.json())


class ThreatObservationView(ObservationHeaderView):
    """Threat observation view,
    as retrieved by :meth:`ThreatObservationsAPI.view`."""

    @property
    def content(self) -> "ThreatObservationContentView":
        """Content."""

        return ThreatObservationContentView(self._get("content"))


class ThreatObservationContentView(JsonObjectView):
    """Threat observation content.

    TODO:
        Implement properties.
    """
