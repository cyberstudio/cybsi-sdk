#!/usr/bin/env python3
from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.pagination import chain_pages

if __name__ == "__main__":
    api_url = "http://127.0.0.1/api"
    auth = APIKeyAuth(api_url, api_key="api_key")
    config = Config(api_url, auth, ssl_verify=False)

    with CybsiClient(config) as client:
        start_page, _ = client.replists.entities("id")
        for item in chain_pages(start_page):
            # Do something with an item
            pass
