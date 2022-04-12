#!/usr/bin/env python3
import uuid
from os import environ

from cybsi.api import Config, CybsiClient

if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    config = Config(api_url, api_key=api_key, ssl_verify=False)
    client = CybsiClient(config)

    reporters = [uuid.uuid4(), uuid.uuid4()]
    dataSources = [uuid.uuid4(), uuid.uuid4()]

    next_cur = ""
    while True:
        generic_observations = client.observations.generics.filter(
            data_source_uuids=reporters,
            reporter_uuids=dataSources,
            cursor=next_cur,
            limit=20,
        )

        [print(x) for x in generic_observations]

        next_cur = generic_observations.cursor
        if next_cur == "":
            break
    client.close()
