#!/usr/bin/env python3
import uuid
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.pagination import chain_pages

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url, api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    reporters = [uuid.uuid4(), uuid.uuid4()]
    dataSources = [uuid.uuid4(), uuid.uuid4()]

    generic_observations = client.observations.generics.filter(
        data_source_uuids=reporters,
        reporter_uuids=dataSources,
        limit=20,
    )

    for obs in chain_pages(generic_observations):
        print(obs)

    client.close()
