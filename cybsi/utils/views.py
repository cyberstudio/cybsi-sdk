import uuid
from typing import List, Optional, Union, cast

from cybsi.api.internal import JsonObjectView
from cybsi.api.observable import (
    AbstractEntityView,
    AttributeNames,
    EntityKeyView,
    EntityTypes,
)


class BasicEntityView(JsonObjectView):
    """Builtin basic entity view.
    Includes only entity type and natual keys.

    .. versionadded:: 2.9
    """

    @property
    def uuid(self) -> uuid.UUID:
        """Entity UUID."""
        return uuid.UUID(self._get("uuid"))

    @property
    def type(self) -> EntityTypes:
        """Entity type."""
        return EntityTypes(self._get("type"))

    @property
    def keys(self) -> List[EntityKeyView]:
        """Entity natural keys."""
        return [EntityKeyView(x) for x in self._get("naturalKeys")]


class PTMSEntityView(AbstractEntityView):
    """Entity view tailored for consumption by PT Multiscanner.

    .. versionadded:: 2.9
    """

    @classmethod
    def _view_uuid(cls) -> uuid.UUID:
        return uuid.UUID("190b4e72-7887-4555-a9a9-6bec33c6529d")

    @property
    def entity(self) -> BasicEntityView:
        """Basic entity view."""
        return BasicEntityView(self._get("entity"))

    @property
    def malware_classes(self) -> Optional[List[str]]:
        """Malware classes.
        Expected, but not required for File entity type.
        :data:`None` for other entity types."""
        return self._map_list_optional("malwareClasses", str)

    @property
    def malware_family(self) -> Optional[str]:
        """Malware family value having the highest confidence.
        Expected, but not required for File entity type.
        :data:`None` for other entity types.
        """
        return self._get_optional("malwareFamily")

    @property
    def related_malware_family(self) -> Optional[str]:
        """Related malware family value having the highest confidence.
        Expected, but not required for DomainName, URL,
        IPAddress, EmailAddress entity types.
        :data:`None` for other entity types."""
        return self._get_optional("relatedMalwareFamily")


class CybsiEntityView(AbstractEntityView):
    """Entity view tailored for consumption by Cybsi-Cybsi relay.

    .. versionadded:: 2.10
    """

    @classmethod
    def _view_uuid(cls) -> uuid.UUID:
        return uuid.UUID("4bd21f23-e4b9-45ab-bde8-078f7115b0b8")

    @property
    def entity(self) -> BasicEntityView:
        """Basic entity view."""
        return BasicEntityView(self._get("entity"))

    @property
    def attribute_values(self) -> List["AttributeValuesView"]:
        """Natural and associated attributes forecast of the entity.

        Natural attributes only from the list:
            For `File` entity type: `Size`, `Names`, `MalwareNames`.
        """

        attributes = self._get("attributeValues")
        return [AttributeValuesView(x) for x in attributes]


class AttributeValuesView(JsonObjectView):
    """Attribute value view."""

    @property
    def name(self) -> AttributeNames:
        """Attribute name."""

        return AttributeNames(self._get("name"))

    @property
    def value(self) -> Union[str, bool, int]:
        """Forecast attribute value.

        Return type depends on attribute name.

        Use :meth:`~cybsi.utils.converters.convert_attribute_value`
            to get attribute value form to create a general observation.
        """

        return self._get("value")

    @property
    def confidence(self) -> float:
        """Attribute confidence."""

        return float(cast(float, self._get("confidence")))
