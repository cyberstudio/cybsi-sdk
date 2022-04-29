#!/usr/bin/env python3
import datetime as dtm
from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient
from cybsi.api.auth import APIKeyForm
from cybsi.api.error import ConflictError
from cybsi.api.observable import ShareLevels
from cybsi.api.user import UserForm
from cybsi.api.user.enums import ResourceName, RoleName

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url, api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)

    ref_key = None
    try:
        # creating new user
        userForm = UserForm(
            login="user_test",
            access_level=ShareLevels.Green,
            roles=[RoleName.EntityReader],
            password="string",
            full_name="Test Tester",
            email="test@pt.com",
        )
        user_ref = client.users.register(userForm)

        # generate API-Key for new user
        apiKeyForm = APIKeyForm(
            description="test key",
            expires_at=dtm.datetime(2022, 6, 1, 0, 0, 0, 0, dtm.timezone.utc),
            permissions=[
                (ResourceName.DataSources, "r"),
                (ResourceName.Observable, "r"),
            ],
        )
        ref_key = client.api_keys.generate(user_uuid=user_ref.uuid, form=apiKeyForm)
    except ConflictError:
        # handle Duplicate Error here
        exit(1)

    print(ref_key)
    # do something with api-key, for example, create new client or save it to file
    client.close()

    auth = APIKeyAuth(api_url, api_key)
    config = Config(api_url, auth, ssl_verify=False)
    client = CybsiClient(config)
