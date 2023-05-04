#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient


def main():
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    # license.zip is zip archive with nested `license-access-token.key`
    f = open("license.zip", "rb")
    client.licenses.upload(f)
    client.close()


if __name__ == "__main__":
    main()
