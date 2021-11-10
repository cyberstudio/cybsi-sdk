from typing import Any, List

from ..common import RefView
from ..internal import JsonObjectForm, JsonObjectView

from .enums import EntityKeyTypes, EntityTypes


class EntityForm(JsonObjectForm):
    """Entity form. Use to register or update an entity.

    Args:
        ent_type: Entity type.
    """

    def __init__(self, ent_type: EntityTypes):
        super().__init__()
        self._data["type"] = ent_type.value

    def add_key(self, key_type: EntityKeyTypes, value: Any) -> "EntityForm":
        """Add natural key to the list of entity keys.

        Args:
            key_type: Key type. Valid values depend on entity type.
            value: Key value. Must be JSON serializable.
        Return:
            Updated entity form.
        """
        keys = self._data.setdefault("keys", [])
        keys.append({"type": key_type.value, "value": value})
        return self


class EntityKeyView(JsonObjectView):
    """Entity key view."""

    @property
    def type(self) -> EntityKeyTypes:
        """Entity key type."""
        return EntityKeyTypes(self._get("type"))

    @property
    def value(self) -> Any:
        """Entity key value.
        Type depends on key type.
        """
        return self._get("value")


class EntityView(RefView):
    """Complete entity view."""

    @property
    def type(self) -> EntityTypes:
        """Entity type."""
        return EntityTypes(self._get("type"))

    @property
    def keys(self) -> List[EntityKeyView]:
        """Entity natural keys."""
        return [EntityKeyView(x) for x in self._get("keys")]
