from cybsi_sdk.client import APIKeyAuth, Config, CybsiClient
from cybsi_sdk.client.pagination import chain_pages

if __name__ == '__main__':
    auth = APIKeyAuth('url', 'key', ssl_verify=False)
    config = Config('url', auth, ssl_verify=False)
    client = CybsiClient(config)

    start_page, _ = client.replists.entities('id')
    for item in chain_pages(start_page):
        # Do something with an item
        pass
