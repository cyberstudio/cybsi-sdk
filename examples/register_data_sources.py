#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.data_source import DataSourceForm, DataSourceTypeForm
from cybsi.api.error import ConflictError

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    ds_type_uuid = None
    ds_uuid = None
    try:  # store datasource_type
        circl_type = DataSourceTypeForm(
            short_name="CIRCL",
            long_name="Computer Incident Response Center Luxembourg",
        )
        ds_type_ref = client.data_source_types.register(circl_type)
        ds_type_uuid = ds_type_ref.uuid
        datasource_form = DataSourceForm(
            type_uuid=ds_type_uuid,
            name="MISP",
            long_name="MISP",
        )
        ds_ref = client.data_sources.register(datasource_form)
        ds_uuid = ds_ref.uuid
    except ConflictError:
        # handle Duplicate Error here
        exit(1)
    view = client.data_sources.view(ds_uuid)
    type_view = client.data_source_types.view(ds_type_uuid)

    client.close()
