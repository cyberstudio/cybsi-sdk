import uuid
from typing import List, Optional

from cybsi.api.internal import JsonObject, JsonObjectView
from cybsi.api.observable import AbstractEntityView, EntityKeyView, EntityTypes


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

    def __init__(self, data: Optional[JsonObject] = None):
        super().__init__(data)

        for attr_value in self._get("attributeValues"):
            self._malware_classes = None
            if attr_value["attribute"] == "MalwareClasses":
                self._malware_classes = attr_value["value"]
            self._malware_families = None
            if attr_value["attribute"] == "MalwareFamilies":
                self._malware_families = attr_value["value"]
            self._related_malware_names = None
            if attr_value["attribute"] == "RelatedMalwareFamilies":
                self._related_malware_names = attr_value["value"]

    @classmethod
    def _view_uuid(cls) -> uuid.UUID:
        return uuid.UUID("190b4e72-7887-4555-a9a9-6bec33c6529d")

    @property
    def entity(self) -> BasicEntityView:
        """Basic entity view."""
        return BasicEntityView(self._get("entity"))

    @property
    def malware_classes(self) -> Optional[str]:
        """Malware classes attribute value.
        Expected, but not required for File entity type.
        :data:`None` for other entity types."""
        return self._malware_classes

    @property
    def malware_families(self) -> Optional[str]:
        """Malware families attribute value.
        Expected, but not required for File entity type.
        :data:`None` for other entity types.
        """
        return self._malware_families

    @property
    def related_malware_families(self) -> Optional[str]:
        """Related malware families attribute value.
        Expected, but not required for DomainName, URL,
        IPAddress, EmailAddress entity types.
        :data:`None` for other entity types."""
        return self._related_malware_names
