from os import environ

from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient
from cybsi_sdk.client.pagination import chain_pages


if __name__ == '__main__':
    api_key = environ.get('CYBSI_API_KEY')
    api_url = environ.get('CYBSI_API_URL')

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    replist_id = 'cabcd58d-9e35-43f8-b2b6-4db9f5bf2bf0'
    page, _ = client.replists.entities(replist_id)

    # Iterate through the pages
    while page:
        print(page.cursor)
        page = page.next_page()

    # Iterate through replist collection elements
    page, _ = client.replists.entities(replist_id)
    for e in chain_pages(page):
        print(e.uuid)
