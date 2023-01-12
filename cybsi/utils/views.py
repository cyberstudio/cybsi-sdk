import uuid
from typing import List, Optional

from cybsi.api.internal import JsonObjectView
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
