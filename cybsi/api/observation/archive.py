from typing import Any, Dict, Iterable, Optional
from uuid import UUID

from ..internal import BaseAPI, JsonObjectView
from ..pagination import Cursor, Page
from .view import ObservationHeaderView


class ArchiveObservationsAPI(BaseAPI):
    """Archive observation API."""

    _path = "/enrichment/observations/archives"

    def filter(
        self,
        *,
        entity_uuid: Optional[UUID] = None,
        artifact_uuid: Optional[UUID] = None,
        data_source_uuids: Optional[Iterable[UUID]] = None,
        reporter_uuids: Optional[Iterable[UUID]] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ArchiveObservationView"]:
        """Get page of filtered observations.

        Page's items are sorted in descending order of observation time.

        Note:
            Calls `GET /enrichment/observations/archives`
        Args:
            artifact_uuid: Artifact identifier.
                Filter archive by specified artifact.
            entity_uuid: Entity identifier.
                Filter archive by specified file entity.
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
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
        """
        params: Dict[str, Any] = {}

        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if entity_uuid is not None:
            params["entityUUID"] = str(entity_uuid)
        if artifact_uuid is not None:
            params["artifactUUID"] = str(artifact_uuid)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, ArchiveObservationView)
        return page

    def view(self, observation_uuid: UUID) -> "ArchiveObservationView":
        """Get the Archive view.

        Note:
            Calls `GET /enrichment/observations/archives/{observation_uuid}`.
        Args:
            observation_uuid: Observation uuid.
        Returns:
            View of the observation.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: observation not found.
        """

        path = f"{self._path}/{observation_uuid}"
        r = self._connector.do_get(path)
        return ArchiveObservationView(r.json())


class ArchiveObservationView(ObservationHeaderView):
    """Archive observation view,
    as retrieved by :meth:`ArchiveObservationsAPI.view`."""

    @property
    def content(self) -> "ArchiveObservationContentView":
        """Content."""

        return ArchiveObservationContentView(self._get("content"))


class ArchiveObservationContentView(JsonObjectView):
    """Archive content.

    TODO:
        Implement properties.
    """
