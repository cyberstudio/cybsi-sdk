#!/usr/bin/env python3
from datetime import datetime, timezone
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.dictionary import DictItemAttributeValue
from cybsi.api.error import SemanticError, SemanticErrorCodes
from cybsi.api.observable import (
    AttributeNames,
    EntityForm,
    EntityKeyTypes,
    EntityTypes,
    ShareLevels,
)
from cybsi.api.observation import GenericObservationForm
from cybsi.api.pagination import chain_pages
from cybsi.api.replist import ReplistForm
from cybsi.api.search.stored_queries import CybsiLangErrorView, StoredQueryForm
from cybsi.utils.views import PTMSEntityView

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    # register generic observation with MalwareClasses/Families attribute facts
    observation = GenericObservationForm(
        share_level=ShareLevels.Green, seen_at=datetime.now(timezone.utc)
    )
    fileEntity = EntityForm(
        EntityTypes.File,
        [(EntityKeyTypes.SHA1, "9ee972c591dc03b24f7bc23c27361dcb719371f2")],
    )
    observation.add_attribute_fact(
        entity=fileEntity,
        attribute_name=AttributeNames.MalwareFamilies,
        value=DictItemAttributeValue(key="Aware"),
        confidence=0.8,
    )
    observation.add_attribute_fact(
        entity=fileEntity,
        attribute_name=AttributeNames.MalwareClasses,
        value=DictItemAttributeValue(key="Trojan"),
        confidence=0.95,
    )
    client.observations.generics.register(observation)

    query_text = "ENT { MalwareClasses = Trojan }"
    try:  # store query
        query_form = StoredQueryForm("malicious entities", query_text)
        query_ref = client.search.stored_queries.register(query_form)
    except SemanticError as exp:
        if exp.code == SemanticErrorCodes.InvalidQueryText:
            e = CybsiLangErrorView.from_semantic_error(exp)
            # handle CybsiLangError here
        exit(1)

    # register new reputation list with given query
    replist = ReplistForm(
        is_enabled=True,
        query_uuid=query_ref.uuid,
        share_level=ShareLevels.Green,
    )
    replist_ref = client.replists.register(replist)
    # view related entities on the PTMSEntityView
    related_entities = client.replists.entities(
        replist_ref.uuid, entity_view=PTMSEntityView
    )
    for ent in chain_pages(related_entities[0]):
        print(ent)

    client.close()

# For file entity RelatedMalwareFamilies attribute value is always null.
# Basic view example:
# {
#     "type": "File",
#     "uuid": "31d8248f-a004-455a-95c2-5c96cba7fae6",
#     "keys": [
#         {
#             "type": "SHA1Hash",
#             "value": "9ee972c591dc03b24f7bc23c27361dcb719371f2"
#         }
#     ]
# }
# PTMS view example:
# {
#     "entity": {
#         "uuid": "31d8248f-a004-455a-95c2-5c96cba7fae6",
#         "type": "File",
#         "naturalKeys": [
#             {
#                 "type": "SHA1Hash",
#                 "value": "9ee972c591dc03b24f7bc23c27361dcb719371f2"
#             }
#         ]
#     },
#     "malwareClasses": [
#       "Ransomware",
#       "Encryptor"
#     ],
#    "malwareFamily": "PlugX",
#    "relatedMalwareFamily": null
# }
# Cybsi-Cybsi view example:
# {
#     "entity": {
#         "uuid": "31d8248f-a004-455a-95c2-5c96cba7fae6",
#         "type": "File",
#         "naturalKeys": [
#             {
#                 "type": "SHA1Hash",
#                 "value": "9ee972c591dc03b24f7bc23c27361dcb719371f2"
#             }
#         ]
#     },
#     "attributeValues": [
#         {
#             "name": "MalwareFamilies",
#             "values": [
#               {
#                   "value": "PlugX",
#                   "confidence": 1
#               }
#             ]
#         }
#     ]
# }
