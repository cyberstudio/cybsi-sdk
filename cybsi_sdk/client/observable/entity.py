from typing import Any

from cybsi_sdk import enums
from cybsi_sdk.client import base


class EntityForm(base.JsonObjectForm):

    def __init__(self, ent_type: enums.EntityTypes):
        super().__init__()
        self._data['type'] = ent_type.value

    def add_key(self,
                key_type: enums.EntityKeyTypes,
                value: Any):
        """Add key to entities form
        """
        keys = self._data.setdefault('keys', [])
        keys.append({'type': key_type.value, 'value': value})
        return self
