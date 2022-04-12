import uuid
import datetime as dtm

from tests import BaseTest
from typing import cast
from unittest.mock import patch
from cybsi.api.api import Tag
from cybsi.api.internal.connector import HTTPConnector
from cybsi.api.user.enums import ResourceName
from cybsi.api.auth.api_key import APIKeysAPI, APIKeyForm


class ApiKeyTest(BaseTest):
    def setUp(self) -> None:
        self.base_url = "http://localhost"
        self.connector = HTTPConnector(base_url=self.base_url, auth=None)
        self.api_keys_api = APIKeysAPI(self.connector)

    @patch.object(HTTPConnector, "do_post")
    def test_api_key_generate(self, mock):
        api_key_generate_form = APIKeyForm(
            dtm.datetime(2022, 6, 1, 0, 0, 0, 0, dtm.timezone.utc),
            "test",
            [
                (ResourceName.DataSources, "r"),
                (ResourceName.Observable, "r"),
            ],
        )

        api_key_generate_response = {
            "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
            "url": "https://test.ru/api-keys/d2209619-2a59-44f7-8d79-caa20fdedbcc",
            "key": "string",
        }

        mock.return_value = self._make_response(201, api_key_generate_response)

        user_uuid = uuid.UUID(int=123)
        res = self.api_keys_api.generate(user_uuid, api_key_generate_form)

        _, kwargs = mock.call_args

        assert f"/users/{user_uuid}/api-keys" == kwargs["path"]
        assert api_key_generate_form.json() == kwargs["json"]

        assert api_key_generate_response["key"] == res.key
        assert api_key_generate_response["id"] == str(res.uuid)
        assert api_key_generate_response["url"] == res.url

    @patch.object(HTTPConnector, "do_get")
    def test_api_key_filter(self, mock):
        api_key_filter_response = [
            {
                "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                "url": "https://test.ru/api-keys/d2209619-2a59-44f7-8d79-caa20fdedbcc",
                "description": "test",
                "createdAt": "2019-08-24T14:15:22.000Z",
                "expiresAt": "2020-09-25T15:16:23.123Z",
                "lastUsedAt": "2021-10-26T16:17:24.456Z",
                "revoked": True,
                "permissions": ["DataSources:r"],
            }
        ]

        mock.return_value = self._make_response(200, api_key_filter_response)
        cursor, link = "FFAAAAAAAB4", "test_link"
        mock.return_value.headers.update(
            {"X-Cursor": cursor, "Link": f"{link}; rel=next"}
        )

        user_uuid = uuid.UUID(int=123)
        res = self.api_keys_api.filter(user_uuid)

        _, kwargs = mock.call_args

        assert f"/users/{user_uuid}/api-keys" == kwargs["path"]

        assert cursor == res.cursor
        assert link == res.next_link

        assert api_key_filter_response[0]["id"] == str(res.data()[0].uuid)
        assert api_key_filter_response[0]["url"] == res.data()[0].url
        assert api_key_filter_response[0]["description"] == res.data()[0].description

        self.assert_timestamp(
            api_key_filter_response[0]["createdAt"],
            res.data()[0].created_at,
        )
        self.assert_timestamp(
            api_key_filter_response[0]["expiresAt"],
            res.data()[0].expires_at,
        )
        self.assert_timestamp(
            api_key_filter_response[0]["lastUsedAt"],
            res.data()[0].last_used_at,
        )

        assert api_key_filter_response[0]["revoked"] == res.data()[0].revoked

        permissions = []
        for raw_perm in api_key_filter_response[0]["permissions"]:
            name, act = raw_perm.split(":", 1)
            permissions.append((ResourceName(name), act))
        assert permissions == res.data()[0].permissions

    @patch.object(HTTPConnector, "do_get")
    def test_api_key_get(self, mock):
        api_key_view_response = {
            "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
            "url": "https://test.ru/api-keys/d2209619-2a59-44f7-8d79-caa20fdedbcc",
            "description": "test",
            "createdAt": "2019-08-24T14:15:22.000Z",
            "expiresAt": "2020-09-25T15:16:23.123Z",
            "lastUsedAt": "2021-10-26T16:17:24.456Z",
            "revoked": True,
            "permissions": ["DataSources:r"],
        }

        mock.return_value = self._make_response(200, api_key_view_response)
        etag = "33a64df551425fcc55e4d42a148795d9f25f89d4"
        mock.return_value.headers.update({"ETag": etag})

        api_key_uuid = uuid.UUID(api_key_view_response["id"])
        res = self.api_keys_api.view(api_key_uuid)

        args, _ = mock.call_args

        assert f"/api-keys/{api_key_uuid}" == args[0]

        assert etag == res.tag

        assert api_key_view_response["id"] == str(res.uuid)
        assert api_key_view_response["url"] == res.url
        assert api_key_view_response["description"] == res.description

        self.assert_timestamp(api_key_view_response["createdAt"], res.created_at)
        self.assert_timestamp(api_key_view_response["expiresAt"], res.expires_at)
        self.assert_timestamp(api_key_view_response["lastUsedAt"], res.last_used_at)

        assert api_key_view_response["revoked"] == res.revoked

        permissions = []
        for raw_perm in api_key_view_response["permissions"]:
            name, act = raw_perm.split(":", 1)
            permissions.append((ResourceName(name), act))
        assert permissions == res.permissions

    @patch.object(HTTPConnector, "do_patch")
    def test_api_key_edit(self, mock):
        api_key_edit_form = {"description": "desc", "revoked": False}

        api_key_uuid = uuid.UUID(int=123)
        tag = cast(Tag, "tag")

        res = self.api_keys_api.edit(
            api_key_uuid,
            tag,
            api_key_edit_form["description"],
            api_key_edit_form["revoked"],
        )

        _, kwargs = mock.call_args

        assert f"/api-keys/{api_key_uuid}", kwargs["path"]
        assert tag == kwargs["tag"]
        assert api_key_edit_form == kwargs["json"]

        assert res is None
