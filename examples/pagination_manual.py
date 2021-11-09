from cybsi.api import APIKeyAuth, Config, CybsiClient


if __name__ == '__main__':
    auth = APIKeyAuth('url', 'key', ssl_verify=False)
    config = Config('url', auth, ssl_verify=False)
    client = CybsiClient(config)

    page, _ = client.replists.entities('id')
    while page:
        # Page is iterable
        for ent in page:
            # Do something with element
            pass
        # Do something with a page
        page = page.next_page()
