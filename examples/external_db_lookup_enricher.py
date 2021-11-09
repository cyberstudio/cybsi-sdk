import time
import uuid

from dataclasses import dataclass
from os import environ
from datetime import datetime, timezone
from typing import cast, List

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.enrichment import (
    AssignedTaskView, CompletedTaskForm,
    ExternalDBLookupParamsView, EnrichmentErrorCodes, EnrichmentTypes,
    FailedTaskForm, TaskResultObservationForm,
)
from cybsi.api.observable import (
    AttributeNames, EntityKeyTypes, EntityTypes, ShareLevels, EntityForm
)
from cybsi.api.observation import GenericObservationForm


def main():
    api_key = environ.get('CYBSI_API_KEY')
    api_url = environ.get('CYBSI_API_URL')

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    wait_on_empty_tasks_sec = 10
    max_task_batch_size = 8

    task_queue = client.enrichment.task_queue

    # Main loop, take a batch of tasks, and handle them.
    while True:
        tasks = task_queue.get_assigned_tasks(max_task_batch_size)
        if tasks:
            handle_task_batch(client, tasks)
        else:
            time.sleep(wait_on_empty_tasks_sec)


def handle_task_batch(
        client: CybsiClient, batch: List[AssignedTaskView]) -> None:
    results = []
    failures = []
    for task in batch:
        try:
            result = enrich_ip(task)
            results.append(result)
        except Exception as ex:
            failures.append(IPEnrichmentTaskFailure(task_id=task.uuid, ex=ex))

    register_results(client, results, failures)


def enrich_ip(task_view: AssignedTaskView) -> 'IPEnrichmentTaskResult':
    # Our enricher expects ExternalDBLookup tasks.
    if task_view.type != EnrichmentTypes.ExternalDBLookup:
        # Shouldn't happen unless Cybsi enrichment rules are mis-configured.
        raise Exception('unexpected enrichment type')

    # As enrichment type is ExternalDBLookup,
    # we can safely cast parameters to a proper type and extract entity.
    lookup = cast(ExternalDBLookupParamsView, task_view.params)
    entity = lookup.entity

    # Our enricher works with IPs only.
    if entity.type != EntityTypes.IP:
        # Shouldn't happen unless Cybsi enrichment rules are mis-configured.
        raise Exception('unexpected entity type')

    # Extract first entity key, it's the only key of IP entity.
    ip_address = entity.keys[0].value

    # Call external system to bring new information about IP.
    # Our imaginary system is a database of IoCs.
    is_ioc = query_external_database(ip_address)

    return IPEnrichmentTaskResult(
        ip=ip_address, task_id=task_view.uuid, is_ioc=is_ioc)


def query_external_database(ip_address: str) -> bool:
    # This could be a network call in actual enricher.
    return True


def register_results(
        client: CybsiClient,
        completed: List['IPEnrichmentTaskResult'],
        failed: List['IPEnrichmentTaskFailure']) -> None:
    # Register definite task failures.
    failed_forms = [
        FailedTaskForm(
            task_uuid=f.task_id,
            error_code=EnrichmentErrorCodes.FatalError,
            message=str(f.ex)
        )
        for f in failed
    ]
    client.enrichment.task_queue.fail_tasks(failed_forms)

    # Register a common observation for all tasks in batch.
    # We could create a separate observation for each entity,
    # but that would be wasteful.
    observation = GenericObservationForm(
        share_level=ShareLevels.Green,
        seen_at=datetime.now(timezone.utc)
    )
    for c in completed:
        # Facts with IsIoC=false are not very useful, don't register them.
        if c.is_ioc:
            entity = EntityForm(EntityTypes.IPAddress)
            entity.add_key(EntityKeyTypes.String, c.ip)
            observation.add_attribute_fact(
                entity=entity,
                attribute_name=AttributeNames.IsIoC,
                value=True,
                confidence=0.9)

    observation_ref = client.observations.generics.register(observation)
    result = TaskResultObservationForm(observation_ref.uuid)

    # Register successfully completed tasks.
    completed_forms = [
        CompletedTaskForm(task_uuid=c.task_id, result=result)
        for c in completed
    ]
    client.enrichment.task_queue.complete_tasks(completed_forms)


@dataclass
class IPEnrichmentTaskResult:
    ip: str
    task_id: uuid.UUID
    is_ioc: bool


@dataclass
class IPEnrichmentTaskFailure:
    task_id: uuid.UUID
    ex: Exception


if __name__ == '__main__':
    main()
