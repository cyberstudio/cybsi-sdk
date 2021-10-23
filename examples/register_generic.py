from os import environ
from datetime import datetime, timezone

from cybsi_sdk import enums
from cybsi_sdk.auth import APIKeyAuth
from cybsi_sdk.client import Config, CybsiClient
from cybsi_sdk.client import observable, observations


def create_generic_observation():
    domain = observable.EntityForm(enums.EntityTypes.DomainName)
    domain.add_key(enums.EntityKeyTypes.String, "test.com")

    observation = observations.GenericObservationForm(
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
    return observation


if __name__ == '__main__':
    api_key = environ.get('CYBSI_API_KEY')
    api_url = environ.get('CYBSI_API_URL')

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    generic_observation = create_generic_observation()
    ref = client.observations.generics.register(generic_observation)
    view = client.observations.generics.view(ref.uuid)
