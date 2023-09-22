from typing import Any

from cybsi_sdk import enums
from cybsi_sdk.client import base


class EntityForm(base.JsonObjectForm):

    def set_type(self, entity_type: enums.EntityTypes):
        """Set entities type
        """
        self._data['type'] = entity_type.value
        return self

    def add_key(self,
                key_type: enums.EntityKeyTypes,
                value: Any):
        """Add key to entities form
        """
        keys = self._data.setdefault('keys', [])
        keys.append({'type': key_type.value, 'value': value})
        return self
