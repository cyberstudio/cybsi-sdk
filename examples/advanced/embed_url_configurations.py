#!/usr/bin/env python3
import uuid
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, embed_object_url=True, ssl_verify=False)

    ds_uuid = uuid.uuid4()
    # create client with embed object URL
    with CybsiClient(config) as client_with_url:
        type_view = client_with_url.data_source_types.view(ds_uuid)
        print(type_view)

    # {
    #   "uuid": "89cb3de7-66ec-4d17-aa85-f42487921b59",
    #   "url": "http://cybsi.ptsecurity.ru/data-source-types/89cb3de7-66ec-4d17-aa85-f42487921b59",
    #   "shortName": "CIRCL",
    #   "longName": "Computer Incident Response Center Luxembourg",
    #   ...
    # }

    # create client without embed object URL
    config.embed_object_url = False
    with CybsiClient(config) as client_without_url:
        type_view = client_without_url.data_source_types.view(ds_uuid)
        print(type_view)

    # {
    #   "uuid": "abc83124-c3ed-4ae7-bea8-ef5addc3094d",
    #   "shortName": "CIRCL",
    #   "longName": "Computer Incident Response Center Luxembourg",
    #   ...
    # }
