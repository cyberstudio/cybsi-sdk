#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.observable import EntityView
from cybsi.api.pagination import Page, chain_pages

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    with CybsiClient(config) as client:
        query = "ENT { IsIoC }"
        search_cursor = client.search.entities.start_search(query)
        page: Page[EntityView] = client.search.entities.next_search_page(
            cursor=search_cursor,
            limit=20,
        )
        for ent in chain_pages(page):
            print(ent)
