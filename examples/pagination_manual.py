#!/usr/bin/env python3
from cybsi.api import Config, CybsiClient

if __name__ == "__main__":
    config = Config("url", api_key="api_key", ssl_verify=False)

    with CybsiClient(config) as client:
        page, _ = client.replists.entities("id")
        while page:
            # Page is iterable
            for ent in page:
                # Do something with element
                pass
            # Do something with a page
            page = page.next_page()
