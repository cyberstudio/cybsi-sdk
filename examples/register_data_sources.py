#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.error import DuplicateDataSourceType
from cybsi.api.data_source import (
    DataSourceForm,
    DataSourceTypeForm,
)

if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    try:  # store datasource_type
        circle_type = DataSourceTypeForm(
            short_name="CIRCL",
            long_name="Computer Incident Response Center Luxembourg",
        )
        ds_type_ref = client.data_source_types.register(circle_type)
        datasource_form = DataSourceForm(
            type_uuid=ds_type_ref.uuid,
            name="MISP",
            long_name="MISP",
        )
        ds_ref = client.data_sources.register(datasource_form)
    except DuplicateDataSourceType:
        # handle Duplicate Error here
        exit(1)
    view = client.data_sources.view(ds_ref.uuid)
    type_view = client.data_source_types.view(ds_type_ref.uuid)
