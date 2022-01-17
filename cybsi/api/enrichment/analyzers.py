"""Use this section of API to operate analyzers.

Analyzers are systems outside Cybsi. They can be queried by Cybsi
for information about artifacts. The result of such query is report.
The reports can contain observations and artifacts. The artifact is a regular file
with additional attributes that can be analyzed or unpacked by the system.
The observation typically provides group of facts obtained after analyzing an artifact.
"""
import uuid
from typing import Any, Dict, List, Optional

from .. import RefView
from ..api import Nullable, Tag, _unwrap_nullable
from ..artifact import ArtifactTypes
from ..data_source import DataSourceCommonView
from ..internal import BaseAPI, JsonObjectForm
from ..pagination import Cursor, Page
from ..view import _TaggedRefView


class AnalyzersAPI(BaseAPI):
    """Analyzers API."""

    _path = "/enrichment/analyzers"

    def view(self, analyzer_uuid: uuid.UUID) -> "AnalyzerView":
        """Get the analyzer view.

        Note:
            Calls `GET /enrichment/analyzers/{analyzer_uuid}`.
        Args:
            analyzer_uuid: Analyzer uuid.
        Returns:
            View of the analyzer.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Analyzer not found.
        """
        path = f"{self._path}/{analyzer_uuid}"
        r = self._connector.do_get(path=path)
        return AnalyzerView(r)

    def register(self, form: "AnalyzerForm") -> RefView:
        """Register analyzer.

        Note:
            Calls `POST /enrichment/analyzers`.
        Args:
            form: Filled analyzer form.
        Returns:
            Reference to analyzer in API.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.ConflictError`:
                An analyzer with such data source is already registered.
        Note:
            Semantic error codes:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())

    def edit(
        self,
        analyzer_uuid: uuid.UUID,
        tag: Tag,
        artifact_types: Optional[List[ArtifactTypes]] = None,
        artifact_size_limit: Nullable[int] = None,
        dashboard_url: Nullable[str] = None,
        task_execution_timeout: Nullable[int] = None,
        task_execution_attempts_count: Nullable[int] = None,
    ) -> None:
        """Edit the analyzer.

        Note:
            Calls `PATCH /enrichment/analyzers/{analyzer_uuid}`.
        Args:
            analyzer_uuid: Analyzer uuid.
            tag: :attr:`AnalyzerView.tag` value. Use :meth:`view` to retrieve it.
            artifact_types: Non-empty artifact types list, if not :data:`None`.
            artifact_size_limit:
                Maximum allowable size of an artifact for analysis, bytes.
                :data:`~cybsi.api.Null` means there is no limit.
                :data:`None` means limit is left unchanged.
            dashboard_url: Analyzer panel link.
                :data:`~cybsi.api.Null` resets dashboard URL to empty value.
                :data:`None` means URL is left unchanged.
            task_execution_timeout: Enricher task execution timeout, sec.
                Timeout must be in range [1;864000].
                :data:`~cybsi.api.Null` means that Cybsi can use default timeout.
                :data:`None` means timeout is left unchanged.
            task_execution_attempts_count:
                The maximum number of attempts to complete the task by the enricher.
                Count must be in range [1;1000].
                :data:`~cybsi.api.Null` means that Cybsi can use default count.
                :data:`None` means that count is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Analyzer not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Analyzer changed since last request. Update tag and retry.
        """
        form: Dict[str, Any] = {}
        if artifact_types is not None:
            form["artifactTypes"] = [t.value for t in artifact_types]
        if artifact_size_limit is not None:
            form["artifactSizeLimit"] = _unwrap_nullable(artifact_size_limit)
        if dashboard_url is not None:
            form["dashboardURL"] = _unwrap_nullable(dashboard_url)
        if task_execution_timeout is not None:
            form["taskExecutionTimeout"] = _unwrap_nullable(task_execution_timeout)
        if task_execution_attempts_count is not None:
            form["taskExecutionAttemptsCount"] = _unwrap_nullable(
                task_execution_attempts_count
            )
        path = f"{self._path}/{analyzer_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)

    def filter(
        self,
        artifact_types: Optional[List[ArtifactTypes]] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["AnalyzerCommonView"]:
        """Get page of filtered analyzers list.

        Note:
            Calls `GET /enrichment/analyzers`
        Args:
            artifact_types: Artifact types list.
                Select analyzers that accept any specified artifact type.
            data_source_uuid: Data source identifier.
                Select analyzers by associated data source identifier.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page of filtered analyzers list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """
        params: Dict[str, Any] = {}

        if artifact_types is not None:
            params["artifactType"] = [t.value for t in artifact_types]
        if data_source_uuid is not None:
            params["dataSourceUUID"] = str(data_source_uuid)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, AnalyzerCommonView)
        return page


class AnalyzerCommonView(RefView):
    """Analyzer common view"""

    @property
    def artifact_types(self) -> List[ArtifactTypes]:
        """Artifact types we can enrich in the analyzer."""
        return [ArtifactTypes(typ) for typ in self._get("artifactTypes")]

    @property
    def artifact_size_limit(self) -> Optional[int]:
        """Maximum allowable size of an artifact for analysis, bytes."""
        return self._get_optional("artifactSizeLimit")

    @property
    def dashboard_url(self) -> Optional[str]:
        """Analyzer panel link."""
        return self._get_optional("dashboardURL")

    @property
    def task_execution_timeout(self) -> Optional[int]:
        """Enricher task execution timeout, sec"""
        return self._get_optional("taskExecutionTimeout")

    @property
    def task_execution_attempts_count(self) -> Optional[int]:
        """The maximum number of attempts to complete the task by the enricher."""
        return self._get_optional("taskExecutionAttemptsCount")

    @property
    def data_source(self) -> "DataSourceCommonView":
        """Data source view representing analyzer."""
        return DataSourceCommonView(self._get("dataSource"))


class AnalyzerView(_TaggedRefView, AnalyzerCommonView):
    pass


class AnalyzerForm(JsonObjectForm):
    """Analyzer form.

    This is the form you need to fill to register analyzer.

    Args:
        data_source_uuid: Data source identifier representing analyzer.
            Unique for analyzer.
        artifact_types: Non-empty artifact types list.
        artifact_size_limit: Maximum allowable size of an artifact for analysis, bytes.
            Empty value means there is no limit.
        dashboard_url: Analyzer panel link.
        task_execution_timeout: Enricher task execution timeout, sec.
            Timeout must be in range [1;864000].
        task_execution_attempts_count: The maximum number of attempts
            to complete the task by the enricher. Count must be in range [1;1000].
    Usage:
        >>> import uuid
        >>> from cybsi.api.enrichment import AnalyzerForm
        >>> from cybsi.api.artifact import ArtifactTypes
        >>> analyzer = AnalyzerForm(
        >>>     data_source_uuid=uuid.UUID("4fd3126f-a0e8-4613-8dc5-cb449641adf2"),
        >>>     entity_types=[ArtifactTypes.FileSample, ArtifactTypes.Archive],
        >>> )
    """

    def __init__(
        self,
        data_source_uuid: uuid.UUID,
        artifact_types: List[ArtifactTypes],
        artifact_size_limit: Optional[int] = None,
        dashboard_url: Optional[str] = None,
        task_execution_timeout: Optional[int] = None,
        task_execution_attempts_count: Optional[int] = None,
    ):
        super().__init__()
        self._data["dataSourceUUID"] = str(data_source_uuid)
        self._data["artifactTypes"] = [typ.value for typ in artifact_types]
        if artifact_size_limit is not None:
            self._data["artifactSizeLimit"] = artifact_size_limit
        if dashboard_url is not None:
            self._data["dashboardURL"] = dashboard_url
        if task_execution_timeout is not None:
            self._data["taskExecutionTimeout"] = task_execution_timeout
        if task_execution_attempts_count is not None:
            self._data["taskExecutionAttemptsCount"] = task_execution_attempts_count
