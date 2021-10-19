Cybsi python SDK
----------------

Software development kit for working with CYBSI API.


### Pagination
Cybsi SDK provides two ways to traverse collections. The **first** way is pages traversing.
This approach fits for cases when you need to get page's properties i.e. cursor.
For walking by page elements just iterate through the page.

```python
from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient

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
```
The **second** way is elements traversing. This approach allows you to iterate through
collections without working with pages. To work with collections as with iterator use `chain_pages`.

```python
from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient
from cybsi_sdk.client.pagination import chain_pages

if __name__ == '__main__':
    auth = APIKeyAuth('url', 'key', ssl_verify=False)
    config = Config('url', auth, ssl_verify=False)
    client = CybsiClient(config)
    
    start_page, _ = client.replists.entities('id')
    for item in chain_pages(start_page):
        # Do something with an item
        pass
```

### Examples

#### Register generic observation

```python
from datetime import datetime, timezone

from cybsi_sdk import enums
from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient
from cybsi_sdk.client import observable, observations

if __name__ == '__main__':
    domain = observable.EntityForm(enums.EntityTypes.DomainName)
    domain.add_key(enums.EntityKeyTypes.String, "test.com")

    generic = observations.GenericObservationForm(
        share_level=enums.ShareLevels.Green,
        seen_at=datetime.now(timezone.utc)
    ).add_attribute_fact(
        entity=domain,
        attribute_name=enums.AttributeNames.IsIoC,
        value=True,
        confidence=0.9
    ).add_attribute_fact(
        entity=domain,
        attribute_name=enums.AttributeNames.IsMalicious,
        value=True,
        confidence=0.9
    )

    api_key = "api-key"
    api_url = "https://cybsi-api.com"

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)
    client.observations.generics.register(generic)
```
