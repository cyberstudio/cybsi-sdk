from typing import Any, List

from cybsi_sdk import enums
from cybsi_sdk.client import base


class EntityForm(base.JsonObjectForm):
    """Entity form. Use to register or update an entity"""
    def __init__(self, ent_type: enums.EntityTypes):
        super().__init__()
        self._data['type'] = ent_type.value

    def add_key(self,
                key_type: enums.EntityKeyTypes,
                value: Any):
        """Add key to entity
        """
        keys = self._data.setdefault('keys', [])
        keys.append({'type': key_type.value, 'value': value})
        return self


class EntityKeyView(base.JsonObjectView):
    """Short entity view"""
    @property
    def type(self) -> enums.EntityKeyTypes:
        return enums.EntityKeyTypes(self._get('type'))

    @property
    def value(self) -> Any:
        return self._get('value')


class EntityView(base.RefView):
    """Complete entity view"""
    @property
    def type(self) -> enums.EntityTypes:
        return enums.EntityTypes(self._get('type'))

    @property
    def keys(self) -> List[EntityKeyView]:
        return [EntityKeyView(x) for x in self._get('keys')]
