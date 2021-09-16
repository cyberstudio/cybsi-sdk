import datetime

from typing import List, Any

from cybsi_sdk import enums
from cybsi_sdk.client import base
from cybsi_sdk.client import observable


class GenericObservationForm(base.JsonObjectForm):

    def __init__(self,
                 share_level: enums.ShareLevels,
                 seen_at: datetime.datetime):
        super().__init__()
        self._data['shareLevel'] = share_level.value
        self._data['seenAt'] = seen_at.isoformat()

    @property
    def _content(self):
        return self._data.setdefault('content', {})

    def set_data_source(self, source_uuid: str):
        """Set data source
        """

        self._data['dataSourceUUID'] = source_uuid
        return self

    def add_attribute_fact(self,
                           entity: observable.EntityForm,
                           attribute_name: enums.AttributeNames,
                           value: Any,
                           confidence: float):
        """Add attribute value fact to observations
        """
        attribute_facts = self._content.setdefault('entityAttributeValues', [])
        attribute_facts.append({
            'entity': entity.json(),
            'attributeName': attribute_name.value,
            'value': value,
            'confidence': confidence,
        })
        return self


class GenericObservationView(base.ResponseView):

    @property
    def reporter(self) -> base.RefView:
        """Get observations reporter
        """

        return base.RefView(self._data.get('reporter'))

    @property
    def data_source(self) -> base.RefView:
        """Get observations data source
        """

        return base.RefView(self._data.get('dataSource'))

    @property
    def share_level(self) -> str:
        """Get observations share level
        """

        return self._data.get('shareLevel')

    @property
    def seen_at(self) -> str:
        """Get observations seenAt
        """

        return self._data.get('seenAt')

    @property
    def registered_at(self):
        """Get observations RegisteredAt
        """

        return self._data.get('registeredAt')

    @property
    def content(self) -> '_ContentView':
        """Get observations content
        """

        return _ContentView(self._data.get('content'))


class _ContentView(dict):

    @property
    def expires_at(self) -> str:
        """Get expiresAt
        """

        return self.get('expiresAt')

    @property
    def entity_relationships(self) -> List['_RelationshipView']:
        """Get entityRelationships
        """

        relationships = self.get('entityRelationships', [])
        return [_RelationshipView(x) for x in relationships]

    @property
    def entity_attribute_values(self) -> List['_AttributeValueView']:
        """Get entityAttributeValues
        """

        attributes = self.get('entityAttributeValues', [])
        return [_AttributeValueView(x) for x in attributes]


class _RelationshipView(dict):
    @property
    def source(self) -> dict:
        """Get relationship's source
        """

        # TODO: implement entities view
        return self.get('source')

    @property
    def kind(self) -> str:
        """Get relationship's kind
        """

        return self.get('kind')

    @property
    def target(self) -> dict:
        """Get target
        """

        return self.get('target')

    @property
    def confidence(self) -> float:
        """Get confidence
        """

        return self.get('confidence')


class _AttributeValueView(dict):

    @property
    def entity(self) -> dict:
        """Get entities view
        """

        return self.get('entities')

    @property
    def attribute_name(self):
        """Get attributeName
        """

        return self.get('attributeName')

    @property
    def value(self) -> Any:
        """Get value
        """

        return self.get('value')

    @property
    def confidence(self) -> float:
        """Get confidence
        """

        return self.get('confidence')
