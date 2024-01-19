#!/usr/bin/env python3
import asyncio
import uuid
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiAsyncClient
from cybsi.api.observable import ShareLevels
from cybsi.api.report import ReportForm


def create_report(observation_uuid, artifact_uuid):
    report = (
        ReportForm(
            ShareLevels.Green,
            description="Report with observation and artifact",
            title="Report",
        )
        .add_observation(observation_uuid)
        .add_artifact(artifact_uuid)
    )
    return report


async def main():
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)

    # Tuples with previously registered artifacts and observation
    # See generic_registration.py and artifact_multipart_upload.py for example.
    observation_artifact_pair = [
        (uuid.uuid4(), uuid.uuid4()),
        (uuid.uuid4(), uuid.uuid4()),
        (uuid.uuid4(), uuid.uuid4()),
    ]
    reports = [create_report(obs, art) for obs, art in observation_artifact_pair]

    # There is also a sync reports registration. Use CybsiClient class:
    #     with CybsiClient(config) as client:
    #         report = create_report(obs_uuid, artifact_uuid)
    #         ref = client.reports.register(report)

    async with CybsiAsyncClient(config) as client:
        registrations = [client.reports.register(r) for r in reports]

        results = await asyncio.gather(*registrations)
        uuids = ", ".join(str(u.uuid) for u in results)

        print(f"Registered reports: {uuids}")


if __name__ == "__main__":
    asyncio.run(main())
