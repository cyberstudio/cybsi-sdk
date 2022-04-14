#!/usr/bin/env python3
from cybsi.api import APIKeyAuth, Config, CybsiClient

if __name__ == "__main__":
    api_url = "http://127.0.0.1/api"
    auth = APIKeyAuth(api_url, api_key="api_key")
    config = Config(api_url, auth, ssl_verify=False)

    with CybsiClient(config) as client:
        page, _ = client.replists.entities("id")
        while page:
            # Page is iterable
            for ent in page:
                # Do something with element
                pass
            # Do something with a page
            page = page.next_page()
