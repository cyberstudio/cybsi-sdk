#!/usr/bin/env python3
import asyncio
from datetime import datetime, timezone
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiAsyncClient
from cybsi.api.observable import (
    AttributeNames,
    EntityForm,
    EntityKeyTypes,
    EntityTypes,
    RelationshipKinds,
    ShareLevels,
)
from cybsi.api.observation import GenericObservationForm


def create_generic_observation(domain, ip):
    domain = EntityForm(
        EntityTypes.DomainName,
        [(EntityKeyTypes.String, domain)],
    )
    ip_address = EntityForm(
        EntityTypes.IPAddress,
        [(EntityKeyTypes.String, ip)],
    )

    observation = (
        GenericObservationForm(
            share_level=ShareLevels.Green, seen_at=datetime.now(timezone.utc)
        )
        .add_attribute_fact(
            entity=domain,
            attribute_name=AttributeNames.IsIoC,
            value=True,
            confidence=0.9,
        )
        .add_attribute_fact(
            entity=domain,
            attribute_name=AttributeNames.IsMalicious,
            value=True,
            confidence=0.9,
        )
        .add_entity_relationship(
            source=domain,
            kind=RelationshipKinds.ResolvesTo,
            target=ip_address,
            confidence=0.5,
        )
    )
    return observation


async def main():
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key)
    config = Config(api_url, auth, ssl_verify=False)

    domain_ip_pairs = [
        ("aa.com", "7.7.7.7"),
        ("bb.com", "8.8.8.8"),
        ("cc.com", "9.9.9.9"),
    ]
    generics = [
        create_generic_observation(domain, ip) for domain, ip in domain_ip_pairs
    ]

    async with CybsiAsyncClient(config) as client:
        registrations = [client.observations.generics.register(g) for g in generics]

        results = await asyncio.gather(*registrations)
        uuids = ", ".join(str(u.uuid) for u in results)

        print(f"Registered observations: {uuids}")


if __name__ == "__main__":
    asyncio.run(main())
