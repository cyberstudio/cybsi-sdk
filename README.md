Cybsi python SDK
----------------

Software development kit for working with CYBSI API.

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
