#!/usr/bin/env python3
import asyncio
from os import environ
from typing import AsyncIterator

import aiofiles
import aiohttp

from cybsi.api import APIKeyAuth, Config, CybsiAsyncClient
from cybsi.api.artifact.enums import ArtifactTypes


async def upload_local_file(client: CybsiAsyncClient):
    # Create test file with 1MB size
    chunk_size = 1024
    file_size = 1024 * chunk_size
    file_name = "test.txt"
    create_file(file_name, file_size)

    # Upload file as async bytes iterator
    async_iter_ref = await client.artifacts.upload(
        filename=file_name,
        data=async_file_iter(file_name, chunk_size),
        data_size=file_size,
        artifact_type=ArtifactTypes.FileSample,
    )
    print(async_iter_ref)


def create_file(file_name: str, file_size: int) -> None:
    with open(file_name, "wb") as f:
        f.seek(file_size - 1)
        f.write(b"\0")


async def async_file_iter(file_name: str, chunk_size: int) -> AsyncIterator[bytes]:
    async with aiofiles.open(file_name, mode="r") as f:
        while True:
            chunk = await f.read(chunk_size)
            if not chunk:
                return
            yield chunk.encode()


async def upload_remote_file(client: CybsiAsyncClient):
    async with aiohttp.request(
        "GET", "https://nakamotoinstitute.org/static/docs/taoup.pdf"
    ) as resp:
        assert resp.status == 200

        stream_reader_ref = await client.artifacts.upload(
            filename="taoup.pdf",
            data=resp.content,
            data_size=int(resp.headers["Content-Length"]),
            artifact_type=ArtifactTypes.FileSample,
        )
        print(stream_reader_ref)


async def main():
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)

    async with CybsiAsyncClient(config) as client:
        upload_local_file_task = asyncio.create_task(upload_local_file(client))
        upload_remote_file_task = asyncio.create_task(upload_remote_file(client))

        await upload_local_file_task
        await upload_remote_file_task


if __name__ == "__main__":
    asyncio.run(main())
