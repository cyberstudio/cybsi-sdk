import time
import uuid

from dataclasses import dataclass
from datetime import datetime, timezone
from os import environ
from typing import cast

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.artifact import ArtifactTypes, ArtifactView
from cybsi.api.enrichment import (
    ArtifactAnalysisParamsView, AssignedTaskView, CompletedTaskForm,
    FailedTaskForm, TaskResultReportForm,
    EnrichmentErrorCodes, EnrichmentTypes
)
from cybsi.api.observable import (
    AttributeNames, EntityKeyTypes, EntityTypes, ShareLevels, EntityForm
)
from cybsi.api.observation import GenericObservationForm
from cybsi.api.report import ReportForm


def main():
    api_key = environ.get('CYBSI_API_KEY')
    api_url = environ.get('CYBSI_API_URL')

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    wait_on_empty_tasks_sec = 10

    # Main loop, take a task and handle it.
    while True:
        tasks = client.enrichment.task_queue.get_assigned_tasks(limit=1)
        if tasks:
            handle_task(client, tasks[0])
        else:
            time.sleep(wait_on_empty_tasks_sec)


def handle_task(client: CybsiClient, task: AssignedTaskView) -> None:
    try:
        artifact_uuid = get_task_artifact_uuid(task)
        view, content = fetch_artifact(client, artifact_uuid)
        result = analyze_artifact(task.uuid, view, content)
        register_result(client, result)
    except Exception as ex:
        failure = FileSampleAnalysisTaskFailure(task_id=task.uuid, ex=ex)
        register_failure(client, failure)


def get_task_artifact_uuid(task_view: AssignedTaskView) -> uuid.UUID:
    # Our enricher expects ArtifactAnalysis tasks.
    if task_view.type != EnrichmentTypes.ArtifactAnalysis:
        # Shouldn't happen unless Cybsi enrichment rules are mis-configured.
        raise Exception('unexpected enrichment type')

    # As enrichment type is ArtifactAnalysis,
    # we can safely cast parameters to a proper type and extract artifact.
    task_params = cast(ArtifactAnalysisParamsView, task_view.params)
    artifact = task_params.artifact

    # Our enricher expects file samples.
    if artifact.type != ArtifactTypes.FileSample:
        # Shouldn't happen unless Cybsi enrichment rules are mis-configured.
        raise Exception('unexpected artifact type')

    return artifact.uuid


def fetch_artifact(client: CybsiClient, artifact_uuid: uuid.UUID):
    artifact_view = client.artifacts.view(artifact_uuid)
    artifact_content = client.artifacts.get_content(artifact_uuid)
    return artifact_view, artifact_content


def analyze_artifact(
        task_id: uuid.UUID,
        view: ArtifactView,
        content) -> 'FileSampleAnalysisTaskResult':
    # ... Call external system to analyze artifact.
    # This is a canned result.
    return FileSampleAnalysisTaskResult(
        task_id=task_id,
        file_md5_hash=view.content.md5_hash,
        is_malicious=True
    )


def register_failure(client, failure: 'FileSampleAnalysisTaskFailure') -> None:
    form = FailedTaskForm(
            task_uuid=failure.task_id,
            error_code=EnrichmentErrorCodes.FatalError,
            message=str(failure.ex)
        )

    client.enrichment.task_queue.fail_tasks([form])


def register_result(
        client: CybsiClient,
        completed: 'FileSampleAnalysisTaskResult') -> None:
    # Register report, it's required for ArtifactAnalysis tasks.
    report_uuid = register_report(client, completed)

    # Mention report in task completion form and send the form.
    result = TaskResultReportForm(report_uuid)
    form = CompletedTaskForm(task_uuid=completed.task_id, result=result)
    client.enrichment.task_queue.complete_tasks([form])


def register_report(
        client: CybsiClient,
        result: 'FileSampleAnalysisTaskResult') -> uuid.UUID:
    observation = GenericObservationForm(
        share_level=ShareLevels.Green,
        seen_at=datetime.now(timezone.utc)
    )
    # Add facts from result to observation
    file_form = EntityForm(EntityTypes.File)
    file_form.add_key(EntityKeyTypes.MD5, result.file_md5_hash)
    if result.is_malicious:
        observation.add_attribute_fact(
            entity=file_form,
            attribute_name=AttributeNames.IsMalicious,
            value=True, confidence=0.9
        )

    observation_ref = client.observations.generics.register(observation)

    report = ReportForm(ShareLevels.Green)

    # ... Add report title, description, external id and other useful meta.

    report.add_observation(observation_ref.uuid)

    report_ref = client.reports.register(report)
    return report_ref.uuid


@dataclass
class FileSampleAnalysisTaskResult:
    task_id: uuid.UUID
    file_md5_hash: str
    is_malicious: bool


@dataclass
class FileSampleAnalysisTaskFailure:
    task_id: uuid.UUID
    ex: Exception


if __name__ == '__main__':
    main()
