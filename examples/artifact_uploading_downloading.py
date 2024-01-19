#!/usr/bin/env python3
import shutil
from io import BytesIO
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient


def main():
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)

    with CybsiClient(config) as client:
        # Upload artifact. We pass BytesIO, but any file-like object will do.
        content = BytesIO(b"artifact content")
        recognized_type_view = client.artifacts.recognize_type(content)

        print(recognized_type_view.type)
        # FileSample
        print(recognized_type_view.format_description)
        # ASCII text, with no line terminators

        content.seek(0)
        artifact_ref = client.artifacts.upload(
            "example.txt", content, artifact_type=recognized_type_view.type
        )

        # Get artifact content, copy in memory and print plain content
        # Also you can download artifact content as ZIP archive (protected by password),
        with client.artifacts.get_content(artifact_ref.uuid) as content:
            buffer = BytesIO()
            shutil.copyfileobj(content.stream, buffer, length=1024 * 1024)
        print("plain artifact content: ", buffer.getvalue())


if __name__ == "__main__":
    main()
