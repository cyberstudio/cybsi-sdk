from typing import Iterable, List, Optional, Tuple

from .. import RefView
from ..internal import JsonObject, JsonObjectForm, JsonObjectView
from .aggregate_section import (
    AttributeValuableFactView,
    AttributeValueView,
    SectionsView,
    _convert_attribute_value_type,
)
from .enums import AttributeNames, EntityKeyTypes, EntityTypes


class EntityForm(JsonObjectForm):
    """Entity form. Use to register or update an entity.

    Args:
        ent_type: Entity type.
        ent_keys: Entity natural keys.
    """

    def __init__(
        self, ent_type: EntityTypes, ent_keys: Iterable[Tuple[EntityKeyTypes, str]] = []
    ):
        super().__init__()
        self._data["type"] = ent_type.value
        keys = self._data.setdefault("keys", [])
        keys.extend({"type": t.value, "value": v} for t, v in ent_keys)

    def add_key(self, key_type: EntityKeyTypes, value: str) -> "EntityForm":
        """Add natural key to the list of entity keys.

        Args:
            key_type: Key type. Valid values depend on entity type.
            value: Key value.
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
    def value(self) -> str:
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


class EntityAggregateView(EntityView):
    """Entity aggregated view."""

    @property
    def sections(self) -> SectionsView:
        """Entity aggregated sections."""
        return SectionsView(self._get("sections"))


class EntityAttributeForecastView(JsonObjectView):
    """Entity attribute forecast view."""

    def __init__(self, data: JsonObject, attribute_name: AttributeNames):
        super().__init__(data)
        self._attribute_name = attribute_name

    @property
    def has_conflicts(self) -> bool:
        """Entity has conflicting facts about attribute."""
        return self._get("hasConflicts")

    @property
    def values(self) -> List["AttributeForecastView"]:
        """Attribute values forecast in descending order of confidence."""
        return [
            AttributeForecastView(x, self._attribute_name) for x in self._get("values")
        ]


class AttributeForecastView(JsonObjectView):
    """Single attribute value forecast."""

    def __init__(self, data: JsonObject, attribute_name: AttributeNames):
        super().__init__(data)
        self._attribute_name = attribute_name

    @property
    def value(self) -> AttributeValueView:
        """Return value type depends on attribute.

        Note:
            Return :class:`~cybsi.api.RefView` type
            is used to get the value of a dictionary item attribute.
            You can resolve the ref
            using :meth:`~cybsi.api.dictionary.DictionariesAPI.view_item`.
        """
        return _convert_attribute_value_type(self._attribute_name, self._get("value"))

    @property
    def confidence(self) -> float:
        """Confidence of forecast."""
        return self._get("confidence")

    @property
    def valuable_facts(self) -> Optional[List[AttributeValuableFactView]]:
        """List of forecast valuable facts in descending order of confidence."""
        values = self._get_optional("valuableFacts")
        if values is not None:
            return [
                AttributeValuableFactView(value, self._attribute_name)
                for value in values
            ]
        return None
