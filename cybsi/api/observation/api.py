from datetime import datetime
from uuid import UUID
from typing import Optional, List, Any, Dict

from .view import ObservationHeaderView
from ..internal import (
    BaseAPI,
    rfc3339_timestamp,
)
from .enums import ObservationTypes
from .generic import GenericObservationsAPI
from ..observable import ShareLevels
from ..pagination import Page


class ObservationsAPI(BaseAPI):
    """Observations API."""

    @property
    def generics(self) -> GenericObservationsAPI:
        """Get generic observation route."""
        return GenericObservationsAPI(self._connector)

    _path = "/enrichment/observations"

    def search(
        self,
        types: Optional[List[ObservationTypes]] = None,
        data_source_uuids: Optional[List[UUID]] = None,
        reporter_uuids: Optional[List[UUID]] = None,
        max_share_level: Optional[ShareLevels] = None,
        seen_before: Optional[datetime] = None,
        seen_after: Optional[datetime] = None,
        registered_before: Optional[datetime] = None,
        registered_after: Optional[datetime] = None,
        report_uuid: Optional[UUID] = None,
        entity_uuid: Optional[UUID] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page["ObservationHeaderView"]:
        """Get observation search results page.

        The result elements are sorted in descending order of observation time.

        Note:
            Calls `GET /enrichment/observations`
        Args:
            types: List of observation types.
                Search for observations of only the specified types.
            entity_uuid: Entity identifier.
                Search for observations mentioning the entity.
            report_uuid: Report identifier.
                Search for observations of the report.
            data_source_uuids: List of data source identifiers.
                Search for observations by original data source identifiers.
            reporter_uuids: List of reporter identifiers.
                Search for observations by reporter data source identifiers.
            max_share_level: Max share level.
                Search for observations up to the max access level.
            seen_before: Search for observations seen before the time.
            seen_after: Search for observations seen after the time.
            registered_before: Search for observations registered before the time.
            registered_after: Search for observations registered after the time.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Search results page and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """
        params: Dict[str, Any] = {}

        if types is not None:
            params["type"] = [str(t.value) for t in types]
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if entity_uuid is not None:
            params["entityUUID"] = str(entity_uuid)
        if report_uuid is not None:
            params["reportUUID"] = str(report_uuid)
        if max_share_level is not None:
            params["shareLevel"] = str(max_share_level.value)
        if seen_before is not None:
            params["seenBefore"] = rfc3339_timestamp(seen_before)
        if seen_after is not None:
            params["seenAfter"] = rfc3339_timestamp(seen_after)
        if registered_before is not None:
            params["registeredBefore"] = rfc3339_timestamp(registered_before)
        if registered_after is not None:
            params["registeredAfter"] = rfc3339_timestamp(registered_after)
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=self._path, params=params)
        page = Page(self._connector.do_get, resp, ObservationHeaderView)
        return page
