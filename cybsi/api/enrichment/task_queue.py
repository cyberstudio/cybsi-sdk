"""Use this section of API to implement a custom enricher.

The API allows to fetch tasks assigned to enricher.
It also allows to publish task execution results and errors.

See Also:
    See :ref:`implement-custom-external-db-example`
    for a complete example of enricher capable of IP enrichment.

    See :ref:`implement-custom-analyzer-example`
    for a complete example of enricher capable of File sample enrichment.
"""
import datetime
import uuid
from typing import Iterable, List, Union, cast

from .. import RefView
from ..data_source import DataSourceCommonView
from ..internal import BaseAPI, JsonObjectForm, parse_rfc3339_timestamp
from .enums import EnrichmentErrorCodes, EnrichmentTaskPriorities, EnrichmentTypes
from .tasks import ArtifactAnalysisParamsView, ExternalDBLookupParamsView


class TaskQueueAPI(BaseAPI):
    """Task queue API.

    .. versionadded:: 2.7
    """

    _path = "/enrichment/task-queue"

    def get_assigned_tasks(self, limit: int = 1) -> List["AssignedTaskView"]:
        """Assign a batch of pending enrichment tasks for execution by client.

        .. versionadded:: 2.7

        All returned tasks have status `Executing`.

        Note:
            Calls `POST /enrichment/task-queue/executing-tasks`.
        Args:
            limit: Maximum task batch size.
        Returns:
            A batch of tasks for execution.
        Warning:
            Please wait some time if :meth:`get_assigned_tasks`
            returns empty list before calling it again.
        """
        path = f"{self._path}/executing-tasks"
        r = self._connector.do_post(path=path, json={"limit": limit})
        return [AssignedTaskView(t) for t in r.json()]

    def complete_tasks(self, completed_tasks: Iterable["CompletedTaskForm"]) -> None:
        """Register successful task results.

        .. versionadded:: 2.7

        Note:
            Calls `POST /enrichment/task-queue/completed-tasks`.
        Args:
            completed_tasks: List of filled forms of completed tasks.
        Returns:
            None on successful registration of results.
        Raises:
            :class:`~cybsi.api.error.ForbiddenError`: Enricher cannot report
             result of one of tasks.
            :class:`~cybsi.api.error.SemanticError`: One of forms contains logic errors.
        Note:
            ForbiddenError error codes:
              * :attr:`~cybsi.api.error.ForbiddenErrorCodes.NotOwner`
                -- Task belongs to other enricher.
            SemanticError codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidTaskStatus`
                -- Current task status is not ``Executing``.
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidTaskResult`
                -- Result has a broken link to observation, report or artifact.
        """
        path = f"{self._path}/completed-tasks"
        task_jsons = [r.json() for r in completed_tasks]
        self._connector.do_post(path=path, json={"tasks": task_jsons})

    def fail_tasks(self, failed_tasks: Iterable["FailedTaskForm"]) -> None:
        """Register failed task errors.

        .. versionadded:: 2.7

        Note:
            Calls `POST /enrichment/task-queue/failed-tasks`.
        Args:
            failed_tasks: List of filled forms of failed tasks.
        Returns:
            None on successful registration of errors.
        Raises:
            :class:`~cybsi.api.error.ForbiddenError`: Enricher cannot report
             result of one of tasks.
            :class:`~cybsi.api.error.SemanticError`: One of forms contains logic errors.
        Note:
            ForbiddenError codes:
              * :attr:`~cybsi.api.error.ForbiddenErrorCodes.NotOwner`
                -- Task belongs to other enricher.
            SemanticError codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidTaskStatus`
                -- Current task status is not ``Executing``.
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidErrorCode`
                -- Error code is invalid for tasks of such type.
        """
        path = f"{self._path}/failed-tasks"
        task_jsons = [r.json() for r in failed_tasks]
        self._connector.do_post(path=path, json={"tasks": task_jsons})


EnrichmentTaskQueueParamsView = Union[
    ArtifactAnalysisParamsView, ExternalDBLookupParamsView
]


class AssignedTaskView(RefView):
    """Task assigned to enricher for execution."""

    _param_types = {
        EnrichmentTypes.ArtifactAnalysis: ArtifactAnalysisParamsView,
        EnrichmentTypes.ExternalDBLookup: ExternalDBLookupParamsView,
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
    def data_source(self) -> DataSourceCommonView:
        """Data source associated with enricher."""
        return DataSourceCommonView(self._get("dataSource"))

    @property
    def type(self) -> "EnrichmentTypes":
        """Enrichment type.

        Note:
            Possible values are subset of :class:`.enums.EnrichmentTypes` values.
            Only :attr:`.enums.EnrichmentTypes.ArtifactAnalysis` and
            :attr:`.enums.EnrichmentTypes.ExternalDBLookup` are possible here.
        """  # noqa: E501
        return EnrichmentTypes(self._get("type"))

    @property
    def params(self) -> EnrichmentTaskQueueParamsView:
        """Parameters of task. Determine exact type of parameters
        using property :attr:`type`.

        If enricher was a function, this would be function parameters.

        Usage:
            >>> from typing import cast
            >>> from cybsi.api.enrichment import (
            >>>     AssignedTaskView, EnrichmentTypes,
            >>>     ExternalDBLookupParamsView
            >>> )
            >>> task_view = AssignedTaskView()
            >>> if task_view.type == EnrichmentTypes.ExternalDBLookup:
            >>>     lookup = cast(ExternalDBLookupParamsView, task_view.params)
            >>>     print(lookup.entity)
        """
        params = self._param_types[self.type](self._get("params"))
        return cast(EnrichmentTaskQueueParamsView, params)


class CompletedTaskForm(JsonObjectForm):
    """Completed task form. Use to register successful task result.

    Args:
        task_uuid: Assigned task uuid.
        result: Task result, type depends on enrichment type.

          * For :attr:`.enums.EnrichmentTypes.ExternalDBLookup`
            provide :class:`TaskResultObservationForm`.
          * For :attr:`.enums.EnrichmentTypes.ArtifactAnalysis`
            provide :class:`TaskResultReportForm`.

    """  # noqa: E501

    def __init__(self, task_uuid: uuid.UUID, result: "TaskResultForm"):
        super().__init__()
        self._data["uuid"] = str(task_uuid)
        self._data["result"] = result.json()


class TaskResultObservationForm(JsonObjectForm):
    """Enrichment result containing observation.

    Use Observations API to register observation and get its uuid.

    Args:
        observation_uuid: Previously registered observation uuid.
    """

    def __init__(self, observation_uuid: uuid.UUID):
        super().__init__()
        self._data["observation"] = {"uuid": str(observation_uuid)}


class TaskResultReportForm(JsonObjectForm):
    """Enrichment result containing report.

    Use Report API to register report and get its uuid.

    Args:
        report_uuid: Previously registered report uuid.
    """

    def __init__(self, report_uuid: uuid.UUID):
        super().__init__()
        self._data["report"] = {"uuid": str(report_uuid)}


class TaskResultArtifactForm(JsonObjectForm):
    """Enrichment result containing artifact.

    Use Artifact API to register report and get its uuid.

    Args:
        artifact_uuid: Previously registered artifact uuid.
    """

    def __init__(self, artifact_uuid: uuid.UUID):
        super().__init__()
        self._data["artifact"] = {"uuid": str(artifact_uuid)}


TaskResultForm = Union[
    TaskResultArtifactForm, TaskResultObservationForm, TaskResultReportForm
]


class FailedTaskForm(JsonObjectForm):
    """Failed enrichment task form.

    Args:
        task_uuid: UUID of task assigned for execution.
        error_code: Enrichment error code.
        message: Error message.
    """

    def __init__(
        self,
        task_uuid: uuid.UUID,
        error_code: "EnrichmentErrorCodes",
        message: str,
    ) -> None:

        super().__init__()
        self._data["uuid"] = str(task_uuid)
        self._data["error"] = {
            "code": error_code.value,
            "message": message,
        }
