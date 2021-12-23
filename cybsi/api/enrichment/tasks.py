"""Use this section of API operate enrichment tasks.

The API allows to fetch and filter enrichment tasks.
It also allows registering enrichment task to start enrichment forcibly.
"""
import datetime
import uuid

from typing import Optional, Union, cast, Dict, Any

from ..internal import BaseAPI, JsonObjectForm, parse_rfc3339_timestamp
from ..pagination import Page

from .. import RefView
from ..artifact import ArtifactTypes
from ..data_source import DataSourceCommonView
from ..internal import JsonObjectView
from ..observable import EntityView, ShareLevels
from ..observation import ObservationCommonView

from .enums import (
    EnrichmentTypes,
    EnrichmentTaskPriorities,
    EnrichmentTaskStatuses,
    EnrichmentErrorCodes,
)


class TasksAPI(BaseAPI):
    """Enrichment task API."""

    _path = "/enrichment/tasks"

    def register(self, form: "TaskForm") -> RefView:
        """Register enrichment task to start enrichment forcibly.

        Note:
            Calls `POST /enrichment/tasks`.
        Args:
            form: Filled enrichment task form.
        Returns:
            Reference to enrichment task in API.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`: Form values are invalid.
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ArtifactNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EnrichmentNotAllowed`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())

    def view(self, task_uuid: uuid.UUID) -> "TaskView":
        """Get the enrichment task view.

        Note:
            Calls `GET /enrichment/tasks/{task_uuid}`.
        Args:
            task_uuid: enrichment task uuid.
        Returns:
            View of the enrichment task.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Enrichment task not found.
        """
        path = f"{self._path}/{task_uuid}"
        r = self._connector.do_get(path=path)
        return TaskView(r.json())

    def filter(
        self,
        artifact_uuid: Optional[uuid.UUID] = None,
        entity_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page["TaskView"]:
        """Get enrichment task filtration list.

        Returns Pending, Completed and Failed enrichment tasks.

        Note:
            Calls `GET /enrichment/tasks`
        Args:
            cursor: Page cursor.
            limit: Page limit.
            artifact_uuid: Artifact identifier.
            entity_uuid: Entity identifier.
        Returns:
            Page with enrichment tasks and
            cursor allowing to get next batch of enrichment tasks.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Artifact uuid and entity uuid parameters are missing.
                At least one of these parameters must be specified.
        """
        params: Dict[str, Any] = {}
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = str(limit)
        if artifact_uuid:
            params["artifactUUID"] = str(artifact_uuid)
        if entity_uuid:
            params["entityUUID"] = str(entity_uuid)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, TaskView)
        return page


class ArtifactAnalysisParamsForm(JsonObjectForm):
    """Artifact analysis task parameters form.

    Args:
        artifact_uuid: Artifact identifier.
        image_id: Analyzer-specific sandbox identifier (not all data sources).
    """

    def __init__(
        self,
        artifact_uuid: uuid.UUID,
        image_id: Optional[str] = None,
    ):
        super().__init__()
        self._data["artifact"] = {"uuid": str(artifact_uuid)}
        if image_id is not None:
            self._data["imageID"] = image_id


class ArchiveUnpackParamsForm(JsonObjectForm):
    """Archive unpack task parameters form.

    Args:
        artifact_uuid: Artifact identifier.
        register_nested_archive_as_file_sample:
            Flag that determines whether to register attached archives
            as FileSample artifacts during unpacking. Default value is false.
        password: Archive password.
    """

    def __init__(
        self,
        artifact_uuid: uuid.UUID,
        register_nested_archive_as_file_sample: Optional[bool] = False,
        password: Optional[str] = None,
    ):
        super().__init__()
        self._data["artifact"] = {"uuid": str(artifact_uuid)}
        if password is not None:
            self._data["password"] = password
        self._data[
            "registerNestedArchiveAsFileSample"
        ] = register_nested_archive_as_file_sample


class ArtifactDownloadParamsForm(JsonObjectForm):
    """Artifact download task parameters form.

    Args:
        url: URL of the resource to be loaded.
        share_level: Share level.
        artifact_type: Artifact type.
    """

    def __init__(
        self,
        url: str,
        share_level: ShareLevels,
        artifact_type: Optional[ArtifactTypes] = None,
    ):
        super().__init__()
        self._data["url"] = url
        if artifact_type is not None:
            self._data["type"] = artifact_type.value
        self._data["shareLevel"] = share_level


class ExternalDBLookupParamsForm(JsonObjectForm):
    """External database task parameters form.

    Args:
        entity_uuid: Entity identifier.
    Note:
        Entity type depends on the data source.
        The applicability of the data source to given entity types can be verified
        by querying the enrichment configuration.
    """

    def __init__(
        self,
        entity_uuid: uuid.UUID,
    ):
        super().__init__()
        self._data["entity"] = {"uuid": str(entity_uuid)}


DNSLookupParamsForm = ExternalDBLookupParamsForm
""" DNS lookup task parameters form.
    (Alias of :attr:`ExternalDBLookupParamsForm`).

    Args:
        entity_uuid: Entity identifier.
    Note:
        For DNSLookup enrichment type can be only
        IPAddress, DomainName entity types.
"""

WhoisLookupParamsForm = ExternalDBLookupParamsForm
""" Whois lookup task parameters form.
    (Alias of :attr:`ExternalDBLookupParamsForm`).

    Args:
        entity_uuid: Entity identifier.
    Note:
        For WhoisLookup enrichment type can be only
        IPAddress, DomainName entity types.
"""


EnrichmentTaskParamsForm = Union[
    ArchiveUnpackParamsForm,
    ArtifactAnalysisParamsForm,
    ArtifactDownloadParamsForm,
    ExternalDBLookupParamsForm,
    DNSLookupParamsForm,
    WhoisLookupParamsForm,
]


class ArtifactAnalysisParamsView(JsonObjectView):
    """Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArtifactAnalysis`."""  # noqa: E501

    @property
    def artifact(self) -> RefView:
        """Artifact, enrichment target.

        Note:
            Use :class:`~cybsi.api.artifact.api.ArtifactsAPI`
            to retrieve complete artifact information and
            its binary content.
        """
        return RefView(self._get("artifact"))

    @property
    def image_id(self) -> Optional[str]:
        """Analyzer-specific image id."""
        return self._get_optional("imageID")


class ArchiveUnpackParamsView(JsonObjectView):
    """Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArchiveUnpack`."""  # noqa: E501

    @property
    def artifact(self) -> RefView:
        """Artifact, enrichment target.

        Note:
            Use :class:`~cybsi.api.artifact.api.ArtifactsAPI`
            to retrieve complete artifact information and
            its binary content.
        """
        return RefView(self._get("artifact"))

    @property
    def password(self) -> Optional[str]:
        """Archive password."""
        return self._get_optional("password")

    @property
    def register_nested_archive_as_file_sample(self) -> Optional[bool]:
        """Flag that determines whether to register attached archives
        as FileSample artifacts during unpacking."""
        return self._get_optional("registerNestedArchiveAsFileSample")


class ArtifactDownloadParamsView(JsonObjectView):
    """Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArtifactDownload`."""  # noqa: E501

    @property
    def url(self) -> str:
        """URL of the resource to be loaded."""
        return self._get("url")

    @property
    def share_level(self) -> ShareLevels:
        """Share level."""
        return self._get("shareLevel")

    @property
    def type(self) -> Optional[ArtifactTypes]:
        """Artifact type."""
        return self._map_optional("type", ArtifactTypes)


class ExternalDBLookupParamsView(JsonObjectView):
    """Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ExternalDBLookup`."""  # noqa: E501

    @property
    def entity(self) -> EntityView:
        """Entity, enrichment target."""
        return EntityView(self._get("entity"))


DNSLookupParamsView = ExternalDBLookupParamsView
"""Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.DNSLookup`.
    (Alias of :attr:`ExternalDBLookupParamsView`).
"""  # noqa: E501

WhoisLookupParamsView = ExternalDBLookupParamsView
"""Task parameters view of :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.WhoisLookup`.
    (Alias of :attr:`ExternalDBLookupParamsView`).
"""  # noqa: E501

EnrichmentTaskParamsView = Union[
    ArtifactAnalysisParamsView,
    ArtifactDownloadParamsView,
    ArchiveUnpackParamsView,
    ExternalDBLookupParamsView,
    DNSLookupParamsView,
    WhoisLookupParamsView,
]


class ArtifactTaskResultView(JsonObjectView):
    """Artifact result task view for
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArtifactDownload`
    """

    @property
    def artifact(self) -> RefView:
        return RefView(self._get("artifact"))


class ReportTaskResultView(JsonObjectView):
    """Report result task view for
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArtifactAnalysis`
    """

    @property
    def report(self) -> RefView:
        return RefView(self._get("report"))


class ObservationTaskResultView(JsonObjectView):
    """Observation result task view for
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ExternalDBLookup`,
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.DNSLookup`,
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.WhoisLookup`.
    :attr:`~cybsi.api.enrichment.enums.EnrichmentTypes.ArchiveUnpack`.
    """

    @property
    def observation(self) -> ObservationCommonView:
        return ObservationCommonView(self._get("observation"))


EnrichmentTaskResultView = Union[
    ArtifactTaskResultView, ReportTaskResultView, ObservationTaskResultView
]


class EnrichmentTaskErrorView(JsonObjectView):
    """Enrichment task error view."""

    @property
    def code(self) -> EnrichmentErrorCodes:
        """Error code."""
        return EnrichmentErrorCodes(self._get("code"))

    @property
    def message(self) -> str:
        """Error massage."""
        return self._get("message")


class TaskForm(JsonObjectForm):
    """Enrichment task form.

    This is the form you need to fill to register enrichment task.

    Args:
        task_type: Enrichment task type.
        params: Enrichment task params.
        data_source: Data source from which the result is expected.
            Required for ArtifactAnalysis, ExternalDBLookup enrichment type.
    Usage:
        >>> import uuid
        >>> from cybsi.api.enrichment import (
        >>>     EnrichmentTypes, TaskForm,
        >>>     ArchiveUnpackParamsForm
        >>> )
        >>> params = ArchiveUnpackParamsForm(
        >>>     artifact_uuid=uuid.UUID("4f9bc3d5-1f12-427e-bcd2-c83fdd09a90f")
        >>> )
        >>> task = TaskForm(
        >>>     task_type=EnrichmentTypes.ArchiveUnpack,
        >>>     params=params
        >>> )
    """

    def __init__(
        self,
        task_type: EnrichmentTypes,
        params: "EnrichmentTaskParamsForm",
        data_source: Optional[uuid.UUID] = None,
    ):
        super().__init__()
        self._data["type"] = task_type.value
        self._data["params"] = params.json()
        if data_source is not None:
            self._data["dataSource"] = {"uuid": str(data_source)}


class TaskView(RefView):
    """Enrichment task view."""

    _param_types = {
        EnrichmentTypes.ArtifactDownload: ArtifactDownloadParamsView,
        EnrichmentTypes.ArchiveUnpack: ArchiveUnpackParamsView,
        EnrichmentTypes.ArtifactAnalysis: ArtifactAnalysisParamsView,
        EnrichmentTypes.ExternalDBLookup: ExternalDBLookupParamsView,
        EnrichmentTypes.WhoisLookup: ExternalDBLookupParamsView,
        EnrichmentTypes.DNSLookup: ExternalDBLookupParamsView,
    }

    _result_types = {
        EnrichmentTypes.ArtifactDownload: ArtifactTaskResultView,
        EnrichmentTypes.ArchiveUnpack: ObservationTaskResultView,
        EnrichmentTypes.ExternalDBLookup: ObservationTaskResultView,
        EnrichmentTypes.WhoisLookup: ObservationTaskResultView,
        EnrichmentTypes.DNSLookup: ObservationTaskResultView,
        EnrichmentTypes.ArtifactAnalysis: ReportTaskResultView,
    }

    @property
    def priority(self) -> EnrichmentTaskPriorities:
        """Priority."""
        return EnrichmentTaskPriorities(self._get("priority"))

    @property
    def created_at(self) -> datetime.datetime:
        """Date and time of task creation."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def updated_at(self) -> datetime.datetime:
        """Date and time of last task update."""
        return parse_rfc3339_timestamp(self._get("updatedAt"))

    @property
    def data_source(self) -> Optional[DataSourceCommonView]:
        """Data source associated with enricher.

        Not empty for ArtifactAnalysis, ExternalDBLookup enrichment type.
        """
        return self._map_optional("dataSource", DataSourceCommonView)

    @property
    def type(self) -> "EnrichmentTypes":
        """Enrichment type."""
        return EnrichmentTypes(self._get("type"))

    @property
    def params(self) -> "EnrichmentTaskParamsView":
        """Parameters of task. Determine exact type of parameters
        using property :attr:`type`.

        If enricher was a function, this would be function parameters.

        Usage:
            >>> from typing import cast
            >>> from cybsi.api.enrichment import (
            >>>     TaskView, EnrichmentTypes,
            >>>     ExternalDBLookupParamsView
            >>> )
            >>> task_view = TaskView()
            >>> if task_view.type == EnrichmentTypes.ExternalDBLookup:
            >>>     lookup = cast(ExternalDBLookupParamsView, task_view.params)
            >>>     print(lookup.entity)
        """
        params = self._param_types[self.type](self._get("params"))
        return cast(EnrichmentTaskParamsView, params)

    @property
    def status(self) -> EnrichmentTaskStatuses:
        """Enrichment task status."""
        return EnrichmentTaskStatuses(self._get("status"))

    @property
    def error(self) -> Optional["EnrichmentTaskErrorView"]:
        """Enrichment task error.

        Can be filled only if the enrichment task status is Failed or Aborted.
        """
        return self._map_optional("error", EnrichmentTaskErrorView)

    @property
    def result(self) -> "EnrichmentTaskResultView":
        """Result of task. Determine exact type of result
        using property :attr:`type`.

        If enricher was a function, this would be function parameters.

        Usage:
            >>> from typing import cast
            >>> from cybsi.api.enrichment import (
            >>>     TaskView, EnrichmentTypes,
            >>>     ExternalDBLookupParamsView
            >>> )
            >>> task_view = TaskView()
            >>> if task_view.type == EnrichmentTypes.ExternalDBLookup:
            >>>     observation = cast(ObservationTaskResultView, task_view.result)
            >>>     print(observation)
        """
        result = self._result_types[self.type](self._get("result"))
        return cast(EnrichmentTaskResultView, result)
