#!/usr/bin/env python3
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.error import SemanticError, SemanticErrorCodes
from cybsi.api.search.enums import QueryCompatibility
from cybsi.api.search.stored_queries import (
    StoredQueryForm,
    CybsiLangErrorView,
)

if __name__ == "__main__":
    api_key = environ.get("CYBSI_API_KEY")
    api_url = environ.get("CYBSI_API_URL")

    auth = APIKeyAuth(api_url, api_key, ssl_verify=False)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    text = "ENT { IsMalicious }"
    view = client.search.stored_queries.validate(text, QueryCompatibility.Replist)
    if len(view.errors) > 0:
        # erroneous query
        exit(1)  # handle errors here
    if len(view.warnings) > 0:
        # semantic warnings
        # for example: always empty result
        pass  # handle warnings here

    try:  # store query
        query = StoredQueryForm("malicious entities", text)
        ref = client.search.stored_queries.register(query)
    except SemanticError as exp:
        if exp.code == SemanticErrorCodes.InvalidQueryText:
            e = CybsiLangErrorView.from_semantic_error(exp)
            # handle CybsiLangError here
        exit(1)

    # get stored query view
    view = client.search.stored_queries.view(ref.uuid)
