#!/usr/bin/env python3
import uuid
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.pagination import chain_pages
from cybsi.utils.views import PTMSEntityView

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    # There is a File entity with MalwareClasses and MalwareFamilies attributes.
    # Also, there is replist with custom query "ENT { MalwareClasses = Ransomware }".
    # See generic_registration.py and replist_registration.py for example.

    replist_uuid = uuid.uuid4()
    # view related entities on the PTMSEntityView
    related_entities = client.replists.entities(
        replist_uuid, entity_view=PTMSEntityView
    )
    for ent in chain_pages(related_entities[0]):
        print(ent)

    client.close()

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
#
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
#
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
