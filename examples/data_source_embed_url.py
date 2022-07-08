#!/usr/bin/env python3
import random
import string
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.data_source import DataSourceTypeForm, DataSourceTypeView


def register_datasource_type(client: CybsiClient) -> "DataSourceTypeView":
    circl_type = DataSourceTypeForm(
        short_name="CIRCL_"
        + "".join(random.choices(string.ascii_uppercase + string.digits, k=5)),
        long_name="Computer Incident Response Center Luxembourg",
    )
    ref = client.data_source_types.register(circl_type)
    view = client.data_source_types.view(ref.uuid)
    return view


if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, embed_object_url=True, ssl_verify=False)

    # create client with embed object URL
    with CybsiClient(config) as client_embed_url:
        type_view = register_datasource_type(client_embed_url)
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
        type_view = register_datasource_type(client_without_url)
        print(type_view)

    # {
    #   "uuid": "abc83124-c3ed-4ae7-bea8-ef5addc3094d",
    #   "shortName": "CIRCL",
    #   "longName": "Computer Incident Response Center Luxembourg",
    #   ...
    # }
