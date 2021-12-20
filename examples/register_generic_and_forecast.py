#!/usr/bin/env python3
from os import environ
from datetime import datetime, timezone

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.observable import (
    AttributeNames,
    EntityForm,
    EntityKeyTypes,
    EntityTypes,
    ShareLevels,
    RelationshipKinds,
)
from cybsi.api.observation import GenericObservationForm


def create_generic_observation(source_entity: EntityForm, target_entity: EntityForm):
    observation = (
        GenericObservationForm(
            share_level=ShareLevels.Green, seen_at=datetime.now(timezone.utc)
        )
        .add_attribute_fact(
            entity=source_entity,
            attribute_name=AttributeNames.IsIoC,
            value=True,
            confidence=0.9,
        )
        .add_attribute_fact(
            entity=target_entity,
            attribute_name=AttributeNames.IsMalicious,
            value=True,
            confidence=0.9,
        )
        .add_entity_relationship(
            source=source_entity,
            kind=RelationshipKinds.Resolves,
            target=target_entity,
            confidence=0.5,
        )
    )
    return observation


if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    domain = EntityForm(EntityTypes.DomainName)
    domain.add_key(EntityKeyTypes.String, "test.com")
    domain_ref = client.observable.entities.register(domain)

    ip_address = EntityForm(EntityTypes.IPAddress)
    ip_address.add_key(EntityKeyTypes.String, "8.8.8.8")
    ip_address_ref = client.observable.entities.register(ip_address)

    generic_observation = create_generic_observation(domain, ip_address)
    ref = client.observations.generics.register(generic_observation)
    view = client.observations.generics.view(ref.uuid)

    attribute_forecast = client.observable.entities.forecast_attribute_values(
        ip_address_ref.uuid, AttributeNames.IsMalicious
    )
    print(attribute_forecast)

    link_forecast = client.observable.entities.forecast_links(ip_address_ref.uuid)
    print(link_forecast.data()[0])

    relationship_forecast = client.observable.relationships.forecast(
        domain_ref.uuid, ip_address_ref.uuid, RelationshipKinds.Resolves
    )
    print(relationship_forecast)
