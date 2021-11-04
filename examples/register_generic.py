from os import environ
from datetime import datetime, timezone

from cybsi_sdk.client import APIKeyAuth, Config, CybsiClient
from cybsi_sdk.client.observable import EntityForm
from cybsi_sdk.client.observation import GenericObservationForm
from cybsi_sdk.model.observable import (
    AttributeNames, EntityKeyTypes, EntityTypes, ShareLevels
)


def create_generic_observation():
    domain = EntityForm(EntityTypes.DomainName)
    domain.add_key(EntityKeyTypes.String, "test.com")

    observation = GenericObservationForm(
        share_level=ShareLevels.Green,
        seen_at=datetime.now(timezone.utc)
    ).add_attribute_fact(
        entity=domain,
        attribute_name=AttributeNames.IsIoC,
        value=True,
        confidence=0.9
    ).add_attribute_fact(
        entity=domain,
        attribute_name=AttributeNames.IsMalicious,
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
