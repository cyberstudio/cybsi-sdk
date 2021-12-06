#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.error import SemanticError, SemanticErrorCodes
from cybsi.api.observable.enums import ShareLevels
from cybsi.api.search.enums import QueryCompatibility
from cybsi.api.search.stored_queries import (
    StoredQueryForm,
    CybsiLangErrorView,
)
from cybsi.api.replist import ReplistForm


if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    query_text = "ENT { IsMalicious }"
    validate_view = client.search.stored_queries.validate(
        query_text, QueryCompatibility.Replist
    )
    if len(validate_view.errors) > 0:
        # erroneous query
        exit(1)  # handle errors here
    if len(validate_view.warnings) > 0:
        # semantic warnings
        # for example: always empty result
        pass  # handle warnings here

    try:  # store query
        query_form = StoredQueryForm("malicious entities", query_text)
        query_ref = client.search.stored_queries.register(query_form)
    except SemanticError as exp:
        if exp.code == SemanticErrorCodes.InvalidQueryText:
            e = CybsiLangErrorView.from_semantic_error(exp)
            # handle CybsiLangError here
        exit(1)

    # get stored query view
    query_view = client.search.stored_queries.view(query_ref.uuid)
    # register new disabled reputation list with given query
    replist = ReplistForm(
        is_enabled=False,
        query_uuid=query_view.uuid,
        share_level=ShareLevels.White,
    )
    replist_ref = client.replists.register(replist)
    # get replist view and set it enable
    replist_view = client.replists.view(replist_ref.uuid)
    client.replists.edit(
        replist_view.uuid,
        replist_view.tag,
        is_enabled=True,
        share_level=ShareLevels.Green,
    )
