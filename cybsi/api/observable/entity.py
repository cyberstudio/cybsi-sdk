from datetime import datetime
from typing import Any, List, Optional

from .aggregate_section import SectionsView

from .. import RefView
from ..internal import (
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
)

from .enums import EntityKeyTypes, EntityTypes, ShareLevels


class EntityForm(JsonObjectForm):
    """Entity form. Use to register or update an entity.

    Args:
        ent_type: Entity type.
    """

    def __init__(self, ent_type: EntityTypes):
        super().__init__()
        self._data["type"] = ent_type.value

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

    @property
    def has_conflicts(self) -> bool:
        """Entity has conflicting facts about attribute."""
        return self._get("hasConflicts")

    @property
    def values(self) -> List["AttributeForecastView"]:
        """Attribute values forecast in descenging order of confidence."""
        return [AttributeForecastView(x) for x in self._get("values")]


class AttributeForecastView(JsonObjectView):
    """Single attribute value forecast."""

    @property
    def value(self) -> Any:
        """Returned value type depends on attribute."""
        return self._get("value")

    @property
    def confidence(self) -> float:
        """Confidence of forecast."""
        return self._get("confidence")

    @property
    def valuable_facts(self) -> Optional[List["AttributeValuableFactView"]]:
        """List of forecast valuable facts in descending order of confidence."""
        return self._map_list_optional("valuableFacts", AttributeValuableFactView)


class ValuableFactView(JsonObjectView):
    """Valuable fact of forecast view."""

    @property
    def data_source(self) -> Optional[RefView]:
        """Original datasource of fact."""
        ds = self._get_optional("dataSource")
        return None if ds is None else RefView(ds)

    @property
    def share_level(self) -> ShareLevels:
        """Fact share level."""
        return ShareLevels(self._get("shareLevel"))

    @property
    def published_at(self) -> Optional[datetime]:
        """Fact observation time."""
        return self._map_optional("seenAt", parse_rfc3339_timestamp)

    @property
    def confidence(self) -> float:
        """Fact confidence."""
        return self._get("confidence")

    @property
    def final_confidence(self) -> float:
        """Final fact confidence."""
        return self._get("finalConfidence")


class AttributeValuableFactView(ValuableFactView):
    """Valuable fact of attribute forecast view."""

    @property
    def value(self) -> Any:
        """Facts attribute value."""
        return self._get("value")
