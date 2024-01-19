#!/usr/bin/env python3
import uuid
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.observable import AttributeNames, RelationshipKinds

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    # There are IP-Address and DomainName entity with IoC attribute and relationship
    # See generic_registration.py script for example.
    domain_uuid = uuid.uuid4()
    ip_address_uuid = uuid.uuid4()

    # Get IsIoC attribute value forecast of ip-address entity.
    attribute_forecast = client.observable.entities.forecast_attribute_values(
        ip_address_uuid, AttributeNames.IsIoC
    )
    print(attribute_forecast)
    # {
    #   "values": [
    #     {
    #       "value": true,
    #       "confidence": 0.8998864,
    #       "valuableFacts": [
    #         {
    #           "dataSource": {
    #             "url": "http://.../3ab411dc-17ab-4169-8ea6-c08271fca49e",
    #             "uuid": "3ab411dc-17ab-4169-8ea6-c08271fca49e"
    #           },
    #           "shareLevel": "Green",
    #           "seenAt": "2021-12-24T17:50:08+03:00",
    #           "confidence": 0.9,
    #           "value": true,
    #           "finalConfidence": 0.8998864
    #         }
    #       ]
    #     }
    #   ],
    #   "hasConflicts": false
    # }

    # Get link forecasts list of ip-address entity.
    link_forecast = client.observable.entities.forecast_links(ip_address_uuid)
    print(link_forecast.data()[0])
    # {
    #   "link": {
    #     "direction": "Reverse",
    #     "relationKind": "ResolvesTo",
    #     "relatedEntity": {
    #       "type": "DomainName",
    #       "url": "http://.../66fd82a1-c35c-424e-986c-133054bd7797",
    #       "uuid": "66fd82a1-c35c-424e-986c-133054bd7797",
    #       "keys": [
    #         {
    #           "type": "String",
    #           "value": "test.com"
    #         }
    #       ]
    #     }
    #   },
    #   "confidence": 0.4999951
    # }

    # Get forecast of relationship (domain name entity resolves ip-address entity).
    relationship_forecast = client.observable.relationships.forecast(
        source_entity_uuid=domain_uuid,
        target_entity_uuid=ip_address_uuid,
        kind=RelationshipKinds.ResolvesTo,
    )
    print(relationship_forecast)
    # {
    #   "relationship": {
    #     "sourceEntity": {
    #       "type": "DomainName",
    #       "url": "http://.../66fd82a1-c35c-424e-986c-133054bd7797",
    #       "uuid": "66fd82a1-c35c-424e-986c-133054bd7797",
    #       "keys": [
    #         {
    #           "type": "String",
    #           "value": "test.com"
    #         }
    #       ]
    #     },
    #     "relationKind": "ResolvesTo",
    #     "targetEntity": {
    #       "type": "IPAddress",
    #       "url": "http://.../40a13d3f-96d2-4c85-acc5-5657f2ecb69d",
    #       "uuid": "40a13d3f-96d2-4c85-acc5-5657f2ecb69d",
    #       "keys": [
    #         {
    #           "type": "String",
    #           "value": "8.8.8.8"
    #         }
    #       ]
    #     }
    #   },
    #   "confidence": 0.4999951,
    #   "valuableFacts": null
    # }

    print(client.observable.entities.forecast_links_statistic(domain_uuid)[0])
    # {
    #     "linkType": {
    #         "url": "http://.../observable/entities/66fd82a1-c35c-424e-986c-133054bd7797/links?kind=ResolvesTo&relatedEntityType=IPAddress&direction=Forward", # noqa: E501
    #         "linkDirection": "Forward",
    #         "relationKind": "ResolvesTo",
    #         "relatedEntitiesType": "IPAddress"
    #     },
    #     "links": {
    #         "total": 1,
    #         "distributionByConfidence": [
    #             {
    #                 "confidenceRange": [0, 0.1],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.1, 0.2],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.2, 0.3],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.3, 0.4],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.4, 0.5],
    #                 "count": 1
    #             },
    #             {
    #                 "confidenceRange": [0.5, 0.6],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.6, 0.7],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.7, 0.8],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.8, 0.9],
    #                 "count": 0
    #             },
    #             {
    #                 "confidenceRange": [0.9, 1],
    #                 "count": 0
    #             }
    #         ]
    #     }
    # }
    client.close()
