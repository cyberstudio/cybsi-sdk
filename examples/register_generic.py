from datetime import datetime, timezone

from cybsi_sdk import enums
from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient
from cybsi_sdk.client import observable, observations

if __name__ == '__main__':
    domain = observable.EntityForm()
    domain.set_type(enums.EntityTypes.DomainName)
    domain.add_key(enums.EntityKeyTypes.String, "test.com")

    generic = observations.GenericObservationForm()
    generic.set_seen_at(datetime.now(timezone.utc))
    generic.set_share_level(enums.ShareLevels.Green)
    generic.add_attribute_fact(
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

    api_key = "tWhCDi-UTdKd14Boav6W1qKHW2fmLHC8Coz1gXqa3k8"
    api_url = "https://lil-mas-aio.cybsi.ptsecurity.ru"

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    ref = client.observations.generics.register(generic)
    view = client.observations.generics.view(ref.uuid)
    print(view)
