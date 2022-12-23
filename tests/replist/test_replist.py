import uuid
from typing import Any, List, cast
from unittest.mock import patch

from cybsi.api.internal.connector import HTTPConnector
from cybsi.api.observable import (
    AbstractEntityView,
    EntityKeyTypes,
    EntityTypes,
    EntityView,
    NodeRole,
)
from cybsi.api.pagination import Cursor, Page
from cybsi.api.replist import EntitySetChangeView, EntitySetOperations, ReplistsAPI
from tests import BaseTest


class CustomEntityView(AbstractEntityView):
    @classmethod
    def _view_uuid(cls) -> uuid.UUID:
        return uuid.UUID("b7560175-d831-4b86-98db-bbf93d97c905")

    @property
    def entity_type(self) -> EntityTypes:
        return EntityTypes(self._get("type"))

    @property
    def value(self) -> str:
        return self._get("value")

    @property
    def node_role(self) -> NodeRole:
        return NodeRole(self._get("nodeRole"))


class ReplistTest(BaseTest):
    def setUp(self) -> None:
        self.base_url = "http://localhost"
        self.connector = HTTPConnector(base_url=self.base_url, auth=None)
        self.replists_api = ReplistsAPI(self.connector)

    @patch.object(HTTPConnector, "do_get")
    def test_replist_entities_default_view(self, mock) -> None:
        entities_response = [
            {
                "type": "IPAddress",
                "uuid": "8f960b00-220a-4785-b9b9-b993efab9165",
                "keys": [{"type": "String", "value": "171.25.193.77"}],
            }
        ]  # type: List[Any]

        mock.return_value = self._make_response(200, entities_response)

        replist_uuid = uuid.uuid4()
        # GIVEN: Replist containing some entities
        # WHEN: Request the entities
        call_result_page: Page[EntityView]
        call_result_page, cursor = self.replists_api.entities(replist_uuid)

        args, _ = mock.call_args

        assert f"/replists/{replist_uuid}/entities" == args[0]

        ent = entities_response[0]
        parsed = call_result_page.data()[0]

        # THEN: Entities are properly parsed, types are converted to SDK types
        assert uuid.UUID(ent["uuid"]) == parsed.uuid
        assert EntityTypes(ent["type"]) == parsed.type
        assert EntityKeyTypes(ent["keys"][0]["type"]) == parsed.keys[0].type

    @patch.object(HTTPConnector, "do_get")
    def test_replist_entities_custom_view(self, mock) -> None:
        entities_response = [
            {"type": "IPAddress", "value": "171.25.193.77", "nodeRole": "CnC"}
        ]

        mock.return_value = self._make_response(200, entities_response)

        replist_uuid = uuid.uuid4()

        # GIVEN: Replist containing some entities
        # WHEN: Request the entities, require non-basic view
        call_result_page, cursor = self.replists_api.entities(
            replist_uuid, entity_view=CustomEntityView
        )

        args, _ = mock.call_args

        assert f"/replists/{replist_uuid}/entities" == args[0]

        ent = entities_response[0]
        parsed: CustomEntityView = call_result_page.data()[0]

        # THEN: Entity fields are parsed correctly.
        assert EntityTypes(ent["type"]) == parsed.entity_type
        assert ent["value"] == parsed.value
        assert NodeRole(ent["nodeRole"]) == parsed.node_role

    @patch.object(HTTPConnector, "do_get")
    def test_replist_changes_custom_view(self, mock) -> None:
        changes_response = [
            {
                "operation": "Add",
                "entity": {
                    "type": "IPAddress",
                    "value": "171.25.193.77",
                    "nodeRole": "CnC",
                },
            }
        ]  # type: List[Any]

        mock.return_value = self._make_response(200, changes_response)

        replist_uuid = uuid.uuid4()
        cursor = cast(Cursor, "replist-start-cursor")

        # GIVEN: Replist containing some changes
        # WHEN: Request the changes, require non-basic view
        call_result_page: Page[EntitySetChangeView[CustomEntityView]]
        call_result_page = self.replists_api.changes(
            replist_uuid, cursor=cursor, entity_view=CustomEntityView
        )

        args, _ = mock.call_args

        assert f"/replists/{replist_uuid}/changes" == args[0]

        change = changes_response[0]
        ent = change["entity"]
        parsed = call_result_page.data()[0]

        # THEN: Change fields are parsed correctly.
        assert EntitySetOperations(change["operation"]) == parsed.operation
        assert EntityTypes(ent["type"]) == parsed.entity.entity_type
        assert ent["value"] == parsed.entity.value
        assert NodeRole(ent["nodeRole"]) == parsed.entity.node_role
