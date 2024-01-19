#!/usr/bin/env python3
import time
import uuid
from os import environ
from typing import cast

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.observable import EntityView
from cybsi.api.pagination import Cursor, Page, chain_pages
from cybsi.api.replist import EntitySetChangeView

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)
    config = Config(api_url, auth, ssl_verify=False)

    with CybsiClient(config) as client:
        wait_on_empty_changes_sec = 10
        replist_uuid = uuid.uuid4()

        cursor_for_changes: Cursor
        entities_page: Page[EntityView]
        # By requesting entities list we get the last cursor
        # to get reputation list changes.
        # The change cursor starts with the latest change of entity in list.
        # WARNING: It is mandatory that you first obtain all pages
        # of reputation list entities so that you can then monitor the changes.
        entities_page, cursor_for_changes = client.replists.entities(replist_uuid)

        changes_page: Page[EntitySetChangeView[EntityView]]
        while True:
            changes_page = client.replists.changes(
                replist_uuid, cursor=cursor_for_changes
            )
            for item in chain_pages(changes_page):
                # Do something with reputation list changes
                #
                if changes_page.cursor is not None:
                    cursor_for_changes = cast(Cursor, changes_page.cursor)

            # Changes are over, wait and request again with last cursor
            time.sleep(wait_on_empty_changes_sec)
