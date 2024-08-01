import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, cast

from .. import Nullable, RefView
from ..api import _map_nullable
from ..artifact import ArtifactCommonView, ArtifactTypes
from ..internal import (
    BaseAPI,
    BaseAsyncAPI,
    JsonObject,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
    rfc3339_timestamp,
)
from ..observable import EntityView, ShareLevels
from ..observation import (
    DNSLookupObservationContentView,
    GenericObservationContentView,
    NetworkSessionObservationContentView,
    ObservationCommonView,
    ObservationHeaderView,
    ObservationTypes,
    ThreatObservationContentView,
    WhoisLookupObservationContentView,
)
from ..pagination import AsyncPage, Cursor, Page

_REPORTS_PATH = "/enrichment/reports"
_REPORTS_LABEL_PATH = "/enrichment/report-labels"


class ReportsAPI(BaseAPI):
    """Report API."""

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
        r = self._connector.do_post(path=_REPORTS_PATH, json=report.json())
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
        path = f"{_REPORTS_PATH}/{report_uuid}"
        r = self._connector.do_get(path)
        return ReportView(r.json())

    def filter(
        self,
        *,
        file_uuid: Optional[uuid.UUID] = None,
        reporter_uuids: Optional[Iterable[uuid.UUID]] = None,
        data_source_uuids: Optional[Iterable[uuid.UUID]] = None,
        entity_uuids: Optional[Iterable[uuid.UUID]] = None,
        labels: Optional[Iterable[str]] = None,
        analyzed_artifact_uuid: Optional[uuid.UUID] = None,
        title: Optional[str] = None,
        created_before: Optional[datetime] = None,
        created_after: Optional[datetime] = None,
        updated_before: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
        external_id: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ReportHeaderView"]:
        """Get report header filtration list that matches the specified criteria.

        Reports are returned in reverse order of registration time.

        Note:
            Calls `GET /enrichment/reports`.
        Args:
            file_uuid: File identifier.
                Filter reports by the artifact of the observed file
                with the specified identifier.
            reporter_uuids: Reporter identifiers.
                Filter reports by reporter data source identifiers.
            data_source_uuids: Data source identifiers.
                Filter reports by original data source identifiers.
            entity_uuids: entity identifiers.
                Filter reports by at least one of the specified entity.
            labels: Filter reports by any of the specified labels.
                Label case is ignored.
            analyzed_artifact_uuid: Analyzed artifact identifier.
                Filter reports based on analysis of the specified artifact.
            title: Filter reports by specified title. Title case is ignored.
                Allows special symbols '%' and '_'.
                The '%' symbol replaces any number of title symbols.
                The '_' symbol replaces only one title symbol.
                To search for '%' and '_' symbols in the usual sense,
                you need to prepend them with '\'.
            created_before: Filter reports created before the timestamp (inclusive).
            created_after: Filter reports created after the timestamp (inclusive).
            updated_before: Filter reports updated before the timestamp (inclusive).
            updated_after: Filter reports updated after the timestamp (inclusive).
            external_id: Filter reports by their external id. Min length is 1.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of reports list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query arguments contain
                semantic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.FileNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
        """
        params: Dict[str, Any] = {}

        if file_uuid is not None:
            params["fileUUID"] = str(file_uuid)
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if entity_uuids is not None:
            params["entityUUID"] = [str(u) for u in entity_uuids]
        if labels is not None:
            params["label"] = list(labels)
        if analyzed_artifact_uuid is not None:
            params["analyzedArtifactUUID"] = str(analyzed_artifact_uuid)
        if title is not None:
            params["title"] = title
        if created_before is not None:
            params["createdBefore"] = rfc3339_timestamp(created_before)
        if created_after is not None:
            params["createdAfter"] = rfc3339_timestamp(created_after)
        if updated_before is not None:
            params["updatedBefore"] = rfc3339_timestamp(updated_before)
        if updated_after is not None:
            params["updatedAfter"] = rfc3339_timestamp(updated_after)
        if external_id is not None:
            params["externalID"] = external_id
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=_REPORTS_PATH, params=params)
        page = Page(self._connector.do_get, resp, ReportHeaderView)
        return page

    def filter_similar_reports(
        self,
        report_uuid: uuid.UUID,
        *,
        reporter_uuid: Optional[uuid.UUID] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["SimilarReportView"]:
        """Get similar reports filtration list in descending order of similarity.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/similar-reports`.
        Args:
            report_uuid: Report identifier.
            reporter_uuid: Reporter identifier.
                Filter similar reports the reporter data source identifiers.
            data_source_uuid: Data source identifier.
                Filter similar reports the original data source identifiers.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of similar reports list and next page cursor.
        """

        params: Dict[str, Any] = {}
        if reporter_uuid is not None:
            params["reporterUUID"] = str(reporter_uuid)
        if data_source_uuid is not None:
            params["dataSourceUUID"] = str(data_source_uuid)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/similar-reports"
        resp = self._connector.do_get(path, params)
        page = Page(self._connector.do_get, resp, SimilarReportView)
        return page

    def explain_report_similarity(
        self,
        report_uuid: uuid.UUID,
        similar_report_uuid: uuid.UUID,
    ) -> "SimilarReportView":
        """Get information about the similarity of reports.

        Note:
            Report A is similar to report B,
            but not the same as report B is similar report A.
        Note:
            Calls `GET /enrichment/reports/{report_uuid}/similar-reports/{similar_report_uuid}`. # noqa: E501
        Args:
            report_uuid: Report identifier.
            similar_report_uuid: Report identifier for comparison
        Returns:
            View of the report.
        """
        path = f"{_REPORTS_PATH}/{report_uuid}/similar-reports/{similar_report_uuid}"
        r = self._connector.do_get(path)
        return SimilarReportView(r.json())

    def search_labels(
        self,
        prefix: str,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[str]:
        """Get report label filtration list.

        Note:
            Calls `GET /enrichment/report-labels`.
        Args:
            prefix: Label prefix.
                Prefix length must be in range [2;50].
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of reports label list and next page cursor.
        """
        params: Dict[str, Any] = {"prefix": prefix}
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=_REPORTS_LABEL_PATH, params=params)
        page = Page(self._connector.do_get, resp, str)
        return page

    def attach_observations(
        self, report_uuid: uuid.UUID, observation_uuids: Iterable[uuid.UUID]
    ) -> RefView:
        """Attach observations to existing report.

        Note:
            Calls `POST /enrichment/reports/{report_uuid}/observations`.
        Args:
            report_uuid: Report UUID.
            observation_uuids: Observation UUIDs.
        Returns:
            Reference to the report.
        Raises:
            :class:`~cybsi.api.error.ForbiddenError`: Operation was forbidden.
                Most probably because user is not owner of the report.
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ObservationNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UnallowedObservationType`
        """
        form: Dict[str, Any] = {"observations": [str(u) for u in observation_uuids]}

        path = f"{_REPORTS_PATH}/{report_uuid}/observations"
        resp = self._connector.do_post(path=path, json=form)
        return RefView(resp.json())

    def filter_observations(
        self,
        report_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ObservationView"]:
        """Filter observations in the report.
        Observations having share level above user's access level are filtered out.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/observations`.
        Args:
            report_uuid: Report UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of report observations list and next page cursor.
                The list of observations is ordered as in the report.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        """
        params: Dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/observations"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, ObservationView)
        return page

    def attach_artifacts(
        self, report_uuid: uuid.UUID, artifact_uuids: Iterable[uuid.UUID]
    ) -> RefView:
        """Attach artifacts to existing report.

        Note:
            Calls `POST /enrichment/reports/{report_uuid}/artifacts`.
        Args:
            report_uuid: Report UUID.
            artifact_uuids: Artifact UUIDs.
        Returns:
            Reference to the report.
        Raises:
            :class:`~cybsi.api.error.ForbiddenError`: Operation was forbidden.
                Most probably because user is not owner of the report.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
        """
        form: Dict[str, Any] = {"artifacts": [str(u) for u in artifact_uuids]}

        path = f"{_REPORTS_PATH}/{report_uuid}/artifacts"
        resp = self._connector.do_post(path=path, json=form)
        return RefView(resp.json())

    def filter_artifacts(
        self,
        report_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["ArtifactCommonView"]:
        """Filter artifacts in the report.
        Artifacts having share level above user's access level are filtered out.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/artifacts`.
        Args:
            report_uuid: Report UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of report artifacts list and next page cursor.
                The list of artifacts is ordered as in the report.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        """
        params: Dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/artifacts"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, ArtifactCommonView)
        return page


class ReportsAsyncAPI(BaseAsyncAPI):
    """Report asynchronous API."""

    async def register(self, report: "ReportForm") -> RefView:
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
        r = await self._connector.do_post(path=_REPORTS_PATH, json=report.json())
        return RefView(r.json())

    async def view(self, report_uuid: uuid.UUID) -> "ReportView":
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
        path = f"{_REPORTS_PATH}/{report_uuid}"
        r = await self._connector.do_get(path)
        return ReportView(r.json())

    async def filter(
        self,
        *,
        file_uuid: Optional[uuid.UUID] = None,
        reporter_uuids: Optional[Iterable[uuid.UUID]] = None,
        data_source_uuids: Optional[Iterable[uuid.UUID]] = None,
        entity_uuids: Optional[Iterable[uuid.UUID]] = None,
        labels: Optional[Iterable[str]] = None,
        analyzed_artifact_uuid: Optional[uuid.UUID] = None,
        title: Optional[str] = None,
        created_before: Optional[datetime] = None,
        created_after: Optional[datetime] = None,
        updated_before: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
        external_id: Optional[str] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ReportHeaderView"]:
        """Get report header filtration list that matches the specified criteria.

        Reports are returned in reverse order of registration time.

        Note:
            Calls `GET /enrichment/reports`.
        Args:
            file_uuid: File identifier.
                Filter reports by the artifact of the observed file
                with the specified identifier.
            reporter_uuids: Reporter identifiers.
                Filter reports by reporter data source identifiers.
            data_source_uuids: Data source identifiers.
                Filter reports by original data source identifiers.
            entity_uuids: entity identifiers.
                Filter reports by at least one of the specified entity.
            labels: Filter reports by any of the specified labels.
                Label case is ignored.
            analyzed_artifact_uuid: Analyzed artifact identifier.
                Filter reports based on analysis of the specified artifact.
            title: Filter reports by specified title. Title case is ignored.
                Allows special symbols '%' and '_'.
                The '%' symbol replaces any number of title symbols.
                The '_' symbol replaces only one title symbol.
                To search for '%' and '_' symbols in the usual sense,
                you need to prepend them with '\'.
            created_before: Filter reports created before the timestamp (inclusive).
            created_after: Filter reports created after the timestamp (inclusive).
            updated_before: Filter reports updated before the timestamp (inclusive).
            updated_after: Filter reports updated after the timestamp (inclusive).
            external_id: Filter reports by their external id. Min length is 1.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of reports list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query arguments contain
                semantic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.FileNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
        """
        params: Dict[str, Any] = {}

        if file_uuid is not None:
            params["fileUUID"] = str(file_uuid)
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if entity_uuids is not None:
            params["entityUUID"] = [str(u) for u in entity_uuids]
        if labels is not None:
            params["label"] = list(labels)
        if analyzed_artifact_uuid is not None:
            params["analyzedArtifactUUID"] = str(analyzed_artifact_uuid)
        if title is not None:
            params["title"] = title
        if created_before is not None:
            params["createdBefore"] = rfc3339_timestamp(created_before)
        if created_after is not None:
            params["createdAfter"] = rfc3339_timestamp(created_after)
        if updated_before is not None:
            params["updatedBefore"] = rfc3339_timestamp(updated_before)
        if updated_after is not None:
            params["updatedAfter"] = rfc3339_timestamp(updated_after)
        if external_id is not None:
            params["externalID"] = external_id
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = await self._connector.do_get(path=_REPORTS_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, ReportHeaderView)
        return page

    async def filter_similar_reports(
        self,
        report_uuid: uuid.UUID,
        *,
        reporter_uuid: Optional[uuid.UUID] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["SimilarReportView"]:
        """Get similar reports filtration list in descending order of similarity.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/similar-reports`.
        Args:
            report_uuid: Report identifier.
            reporter_uuid: Reporter identifier.
                Filter similar reports the reporter data source identifiers.
            data_source_uuid: Data source identifier.
                Filter similar reports the original data source identifiers.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of similar reports list and next page cursor.
        """

        params: Dict[str, Any] = {}
        if reporter_uuid is not None:
            params["reporterUUID"] = str(reporter_uuid)
        if data_source_uuid is not None:
            params["dataSourceUUID"] = str(data_source_uuid)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/similar-reports"
        resp = await self._connector.do_get(path, params)
        page = AsyncPage(self._connector.do_get, resp, SimilarReportView)
        return page

    async def explain_report_similarity(
        self,
        report_uuid: uuid.UUID,
        similar_report_uuid: uuid.UUID,
    ) -> "SimilarReportView":
        """Get information about the similarity of reports.

        Note:
            Report A is similar to report B,
            but not the same as report B is similar report A.
        Note:
            Calls `GET /enrichment/reports/{report_uuid}/similar-reports/{similar_report_uuid}`. # noqa: E501
        Args:
            report_uuid: Report identifier.
            similar_report_uuid: Report identifier for comparison
        Returns:
            View of the report.
        """
        path = f"{_REPORTS_PATH}/{report_uuid}/similar-reports/{similar_report_uuid}"
        r = await self._connector.do_get(path)
        return SimilarReportView(r.json())

    async def search_labels(
        self,
        prefix: str,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage[str]:
        """Get report label filtration list.

        Note:
            Calls `GET /enrichment/report-labels`.
        Args:
            prefix: Label prefix.
                Prefix length must be in range [2;50].
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of reports label list and next page cursor.
        """
        params: Dict[str, Any] = {"prefix": prefix}
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = await self._connector.do_get(_REPORTS_LABEL_PATH, params=params)
        page = AsyncPage(self._connector.do_get, resp, str)
        return page

    async def attach_observations(
        self, report_uuid: uuid.UUID, observation_uuids: Iterable[uuid.UUID]
    ) -> RefView:
        """Attach observations to existing report.

        Note:
            Calls `POST /enrichment/reports/{report_uuid}/observations`.
        Args:
            report_uuid: Report UUID.
            observation_uuids: Observation UUIDs.
        Returns:
            Reference to the report.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ObservationNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UnallowedObservationType`
        """
        form: Dict[str, Any] = {"observations": [str(u) for u in observation_uuids]}

        path = f"{_REPORTS_PATH}/{report_uuid}/observations"
        resp = await self._connector.do_post(path=path, json=form)
        return RefView(resp.json())

    async def filter_observations(
        self,
        report_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ObservationView"]:
        """Filter observations in the report.
        Observations having share level above user's access level are filtered out.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/observations`.
        Args:
            report_uuid: Report UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of report observations list and next page cursor.
                The list of observations is ordered as in the report.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        """
        params: Dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/observations"
        resp = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, resp, ObservationView)
        return page

    async def attach_artifacts(
        self, report_uuid: uuid.UUID, artifact_uuids: Iterable[uuid.UUID]
    ) -> RefView:
        """Attach artifacts to existing report.

        Note:
            Calls `POST /enrichment/reports/{report_uuid}/artifacts`.
        Args:
            report_uuid: Report UUID.
            artifact_uuids: Artifact UUIDs.
        Returns:
            Reference to the report.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
        """
        form: Dict[str, Any] = {"artifacts": [str(u) for u in artifact_uuids]}

        path = f"{_REPORTS_PATH}/{report_uuid}/artifacts"
        resp = await self._connector.do_post(path=path, json=form)
        return RefView(resp.json())

    async def filter_artifacts(
        self,
        report_uuid: uuid.UUID,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage["ArtifactCommonView"]:
        """Filter artifacts in the report.
        Artifacts having share level above user's access level are filtered out.

        Note:
            Calls `GET /enrichment/reports/{report_uuid}/artifacts`.
        Args:
            report_uuid: Report UUID.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of report artifacts list and next page cursor.
                The list of artifacts is ordered as in the report.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Report not found.
        """
        params: Dict[str, Any] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{_REPORTS_PATH}/{report_uuid}/artifacts"
        resp = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, resp, ArtifactCommonView)
        return page


class ReportForm(JsonObjectForm):
    """Report form.

    Args:
        share_level: Report share level.
        title: Report title.
        description: Report description.
        external_id: ID of the report in external system. Must be unique for datasource.
        created_at: Time of report creation.
            created_at must be not later than published_at.
        published_at: Time of report publication.
            published_at must be not earlier than created_at.
        external_refs: List of external references associated with report.
        labels: List of report labels.
        data_source: UUID of report's associated datasource.
        observation_uuids: List of report's observations.
        artifact_uuids: List of report's artifacts.
        analyzed_artifact_uuid: Analyzed artifact identifier.
    """

    def __init__(
        self,
        share_level: ShareLevels,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        external_id: Optional[str] = None,
        created_at: Nullable[datetime] = None,
        published_at: Nullable[datetime] = None,
        external_refs: Optional[Iterable[str]] = None,
        labels: Optional[Iterable[str]] = None,
        data_source: Optional[uuid.UUID] = None,
        observation_uuids: Optional[Iterable[uuid.UUID]] = None,
        artifact_uuids: Optional[Iterable[uuid.UUID]] = None,
        analyzed_artifact_uuid: Optional[uuid.UUID] = None,
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
            self._data["createdAt"] = _map_nullable(created_at, rfc3339_timestamp)
        if published_at is not None:
            self._data["publishedAt"] = _map_nullable(published_at, rfc3339_timestamp)
        if external_refs is not None:
            self._data["externalRefs"] = list(external_refs)
        if labels is not None:
            self._data["labels"] = list(labels)
        if data_source is not None:
            self._data["dataSource"] = str(data_source)
        if observation_uuids is not None:
            self._data["observations"] = [str(u) for u in observation_uuids]
        if artifact_uuids is not None:
            self._data["artifacts"] = [str(u) for u in artifact_uuids]
        if analyzed_artifact_uuid is not None:
            self._data["analyzedArtifactUUID"] = str(analyzed_artifact_uuid)

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


class ReportHeaderView(RefView):
    """Report header view."""

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
    def created_at(self) -> datetime:
        """Report created time."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def published_at(self) -> datetime:
        """Report publication time."""
        return parse_rfc3339_timestamp(self._get("publishedAt"))

    @property
    def registered_at(self) -> datetime:
        """Report registered time."""
        return parse_rfc3339_timestamp(self._get("registeredAt"))

    @property
    def external_refs(self) -> Optional[List[str]]:
        """List of external references associated with report."""
        return self._get_optional("externalRefs")

    @property
    def labels(self) -> Optional[List[str]]:
        """List of report labels."""
        return self._get_optional("labels")

    @property
    def data_source(self) -> RefView:
        """Original data source of report."""
        return RefView(self._get("dataSource"))

    @property
    def reporter(self) -> RefView:
        """Data source that reported to system."""
        return RefView(self._get("reporter"))

    @property
    def analyzed_artifact_uuid(self) -> Optional[uuid.UUID]:
        """Analyzed artifact UUID."""
        return self._map_optional("analyzedArtifactUUID", uuid.UUID)


class ReportView(ReportHeaderView):
    """Report view."""

    @property
    def artifacts(self) -> Optional[List["ArtifactShortView"]]:
        """Artifacts attached to report."""
        return self._map_list_optional("artifacts", ArtifactShortView)

    @property
    def observations(self) -> Optional[List[ObservationCommonView]]:
        """Observations attached to report."""
        return self._map_list_optional("observations", ObservationCommonView)


class ArtifactShortView(RefView):
    """Artifact short view."""

    @property
    def type(self) -> ArtifactTypes:
        """Artifact type."""
        return self._get("type")


class SimilarReportView(JsonObjectView):
    """Similar report view."""

    @property
    def report(self) -> ReportHeaderView:
        """Report header view."""
        return ReportHeaderView(self._get("report"))

    @property
    def correlation(self) -> "SimilarReportCorrelationView":
        """Report correlation view."""
        return SimilarReportCorrelationView(self._get("correlation"))


class SimilarReportCorrelationView(JsonObjectView):
    """Similar report correlation view."""

    @property
    def similarity(self) -> float:
        """Similarity degree of reports in the range [0;1]
        The larger the value, the greater the degree of coincidence."""
        return self._get("similarity")

    @property
    def matched_entities(self) -> Optional[List["MatchedEntitiesView"]]:
        """List of matched entities."""
        return self._map_list_optional("matchedEntities", MatchedEntitiesView)


class MatchedEntitiesView(JsonObjectView):
    """Matched entity view."""

    @property
    def entity(self) -> EntityView:
        """Entity."""
        return self._get("entity")

    @property
    def weight(self) -> float:
        """Weight value of entity in range [0;1]."""
        return self._get("weight")


class ObservationView(ObservationHeaderView):
    """Observation view."""

    @property
    def content(self) -> "ObservationContentView":
        """Observation content.

        Depends on observation type.

        Using:
            >>> from typing import cast
            >>> from cybsi.api.observation import ObservationTypes
            >>> from cybsi.api.report import ObservationView
            >>> view = ObservationView()
            >>> if view.type == ObservationTypes.Generic:
            >>>     # do something with generic content
            >>>     print(view.content.generic)
        """

        return ObservationContentView(self.type, self._get("content"))


class ObservationContentView:
    """Observation content view."""

    _content_converters = {
        ObservationTypes.DNSLookup: DNSLookupObservationContentView,
        ObservationTypes.Generic: GenericObservationContentView,
        ObservationTypes.NetworkSession: NetworkSessionObservationContentView,
        ObservationTypes.Threat: ThreatObservationContentView,
        ObservationTypes.WhoisLookup: WhoisLookupObservationContentView,
    }

    def __init__(self, obs_type: ObservationTypes, content: JsonObject):
        view = self._content_converters[obs_type]
        self._contents = {obs_type: view(content)}

    @property
    def dns_lookup(self) -> DNSLookupObservationContentView:
        """Content of dns lookup observation.

        Raises:
            :class:`KeyError`:
                Content is absent in the :class:`ObservationContentView`.
        """
        val = cast(
            DNSLookupObservationContentView, self._contents[ObservationTypes.DNSLookup]
        )
        return val

    @property
    def generic(self) -> GenericObservationContentView:
        """Content of generic observation.

        Raises:
            :class:`KeyError`:
                Content is absent in the :class:`ObservationContentView`.
        """
        val = cast(
            GenericObservationContentView, self._contents[ObservationTypes.Generic]
        )
        return val

    @property
    def network_session(self) -> NetworkSessionObservationContentView:
        """Content of network session observation.

        Raises:
            :class:`KeyError`:
                Content is absent in the :class:`ObservationContentView`.
        """
        val = cast(
            NetworkSessionObservationContentView,
            self._contents[ObservationTypes.NetworkSession],
        )
        return val

    @property
    def threat(self) -> ThreatObservationContentView:
        """Content of threat observation.

        Raises:
            :class:`KeyError`:
                Content is absent in the :class:`ObservationContentView`.
        """
        val = cast(
            ThreatObservationContentView, self._contents[ObservationTypes.Threat]
        )
        return val

    @property
    def whois_lookup(self) -> WhoisLookupObservationContentView:
        """Content of whois lookup observation.

        Raises:
            :class:`KeyError`:
                Content is absent in the :class:`ObservationContentView`.
        """
        val = cast(
            WhoisLookupObservationContentView,
            self._contents[ObservationTypes.WhoisLookup],
        )
        return val
