from datetime import datetime

from typing import List, Optional

import uuid

from cybsi.api.artifact.api import ArtifactCommonView
from cybsi.api.observation.api import ObservationCommonView

from ..common import RefView
from ..internal import (
    BaseAPI,
    JsonObjectForm,
    rfc3339_timestamp,
    parse_rfc3339_timestamp,
)
from ..observable import ShareLevels


class ReportsAPI(BaseAPI):
    """Report API."""

    _path = "/enrichment/reports"

    def register(self, report: "ReportForm") -> RefView:
        """Register report.

        Note:
            Calls `POST /enrichment/reports`.
        Args:
            report: Filled report form.
        Returns:
            Reference to the registered report.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.ConflictError`:
                A report with such external_id and data source is already registered.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidTime`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ObservationNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UnallowedObservationType`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
        """
        r = self._connector.do_post(path=self._path, json=report.json())
        return RefView(r.json())

    def view(self, report_uuid: uuid.UUID) -> "ReportView":
        """Get report view.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}`.
        Args:
            report_uuid: Report uuid.
        Returns:
            View of the report.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        """
        path = f"{self._path}/{report_uuid}"
        r = self._connector.do_get(path)
        return ReportView(r.json())


class ReportForm(JsonObjectForm):
    """Report form.

    Args:
        share_level: Report share level.
        title: Report title.
        description: Report description.
        external_id: ID of the report in external system. Must be unique for datasource.
        created_at: Time of report creation.
        published_at: Time of report publication.
        external_refs: List of external references associated with report.
        labels: List of report labels.
        data_source: UUID of report's associated datasource.
    """

    def __init__(
        self,
        share_level: ShareLevels,
        title: Optional[str] = None,
        description: Optional[str] = None,
        external_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        published_at: Optional[datetime] = None,
        external_refs: Optional[List[str]] = None,
        labels: Optional[List[str]] = None,
        data_source: Optional[uuid.UUID] = None,
    ):
        super().__init__()
        self._data["shareLevel"] = share_level.value
        if title is not None:
            self._data["title"] = title
        if description is not None:
            self._data["description"] = description
        if external_id is not None:
            self._data["externalID"] = external_id
        if created_at is not None:
            self._data["createdAt"] = rfc3339_timestamp(created_at)
        if published_at is not None:
            self._data["publishedAt"] = rfc3339_timestamp(published_at)
        if external_refs is not None:
            self._data["externalRefs"] = external_refs
        if labels is not None:
            self._data["labels"] = labels
        if data_source is not None:
            self._data["dataSource"] = str(data_source)

    def add_observation(self, observation_uuid: uuid.UUID) -> "ReportForm":
        """Add observation to report.
        Args:
            observation_uuid: UUID of associated observation.
        Return:
            Updated report form.
        """
        observations = self._data.setdefault("observations", [])
        observations.append(str(observation_uuid))
        return self

    def add_artifact(self, artifact_uuid: uuid.UUID) -> "ReportForm":
        """Add artifact to report.
        Args:
            artifact_uuid: UUID of associated artifact.
        Return:
            Updated report form.
        """
        artifacts = self._data.setdefault("artifacts", [])
        artifacts.append(str(artifact_uuid))
        return self


class ReportView(RefView):
    """Report view."""

    @property
    def share_level(self) -> ShareLevels:
        """Report share level."""
        return ShareLevels(self._get("shareLevel"))

    @property
    def title(self) -> Optional[str]:
        """Report title."""
        return self._get_optional("title")

    @property
    def description(self) -> Optional[str]:
        """Report description."""
        return self._get_optional("description")

    @property
    def external_id(self) -> Optional[str]:
        """Unique external ID for current data source."""
        return self._get_optional("externalID")

    @property
    def created_at(self) -> Optional[datetime]:
        """Report created time."""
        return self._map_optional("createdAt", parse_rfc3339_timestamp)

    @property
    def published_at(self) -> Optional[datetime]:
        """Report publication time."""
        return self._map_optional("publishedAt", parse_rfc3339_timestamp)

    @property
    def registered_at(self) -> Optional[datetime]:
        """Report registered time."""
        return self._map_optional("registeredAt", parse_rfc3339_timestamp)

    @property
    def external_refs(self) -> Optional[List[str]]:
        """List of external references assotiated with report."""
        return self._get_optional("externalRefs")

    @property
    def labels(self) -> Optional[List[str]]:
        """List of report labels."""
        return self._get_optional("labels")

    @property
    def data_source(self) -> Optional[RefView]:
        """Original datasource of report."""
        ds = self._get_optional("dataSource")
        return None if ds is None else RefView(ds)

    @property
    def reporter(self) -> Optional[RefView]:
        """Datasource that reported to system."""
        return self._map_optional("reporter", RefView)

    @property
    def artifacts(self) -> Optional[List[ArtifactCommonView]]:
        """Artifacts attached to report."""
        return self._map_list_optional("artifacts", ArtifactCommonView)

    @property
    def observations(self) -> Optional[List[ObservationCommonView]]:
        """Observations attached to report."""
        return self._map_list_optional("observations", ObservationCommonView)
