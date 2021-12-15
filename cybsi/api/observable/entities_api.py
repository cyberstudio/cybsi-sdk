import uuid
from datetime import datetime
from typing import Optional, List

from cybsi.api.error import JsonObject
from .entity import EntityForm, EntityAggregateView, EntityKeyView

from .enums import EntityTypes, EntityAggregateSections, EntityKeyTypes
from .. import RefView
from ..internal import BaseAPI, rfc3339_timestamp
from ..pagination import Page


class EntitiesAPI(BaseAPI):
    """Entities API."""

    _path = "/observable/entities"
    _path_canonical_key = "/observable/entity-canonical-key"

    def register(self, entity: EntityForm) -> RefView:
        """Register an entity.

        Note:
            Calls `PUT /observable/entities`.
        Args:
            entity: Entity registration form.
        Returns:
            Reference to a registered entity.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKey`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.KeyConflict`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.BrokenKeySet`
        Usage:
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityForm, EntityTypes, EntityKeyTypes
            >>> client: CybsiClient
            >>> entity_form = EntityForm(EntityTypes.DomainName)
            >>> entity_form.add_key(EntityKeyTypes.String, "example.com")
            >>> ref = client.observable.entities.register(entity_form)
            >>> # It's a good idea to use entity uuid in observation forms.
            >>> # But here we simply print returned ref.
            >>> print(ref)
        """
        r = self._connector.do_put(path=self._path, json=entity.json())
        return RefView(r.json())

    def view(
        self,
        entity_uuid: uuid.UUID,
        sections: Optional[List[EntityAggregateSections]] = None,
        forecast_at: Optional[datetime] = None,
        with_valuable_facts: Optional[bool] = None,
    ) -> EntityAggregateView:
        """Get an entity view.

        Note:
            Calls `GET /observable/entities/{query_uuid}`.
        Args:
            entity_uuid: Entity uuid.
            sections: Sections to be aggregated.
            forecast_at: Point of time to aggregate sections at.
            with_valuable_facts: Include valuable facts in response.
        Returns:
            Aggregated view of the entity.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Entity not found.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import (
            >>>     EntityAggregateSections,
            >>>     EntityTypes,
            >>>     EntityKeyTypes
            >>> )
            >>> client: CybsiClient
            >>> filter_sections = [
            >>>     EntityAggregateSections.AssociatedAttributes,
            >>>     EntityAggregateSections.NaturalAttributes,
            >>> ]
            >>> aggregate = client.observable.entities.view(
            >>>    UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>    sections=filter_sections,
            >>>    with_valuable_facts = True
            >>> )
            >>> # Do something with an aggregate
            >>> if aggregate.sections.associated_attributes is not None:
            >>>     for attr in aggregate.sections.associated_attributes.data:
            >>>         print(attr.attribute_name)
        """
        path = f"{self._path}/{entity_uuid}"
        params = {}  # type: JsonObject
        if sections is not None:
            params["section"] = [section.value for section in sections]
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if with_valuable_facts is not None:
            params["valuableFacts"] = with_valuable_facts
        r = self._connector.do_get(path=path, params=params)
        return EntityAggregateView(r.json())

    def aggregate(
        self,
        entity_uuids: List[uuid.UUID],
        sections: Optional[List[EntityAggregateSections]] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page[EntityAggregateView]:
        """Get list of aggregated entities.

        Note:
            Calls `GET /observable/entities`.
        Args:
            entity_uuids: Entity uuids. At least one must be provided.
            sections: Sections to be aggregated.
            forecast_at: Point of time to aggregate sections at.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with aggregated entities views.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>> from cybsi.api.observable import (
            >>>     EntityAggregateSections,
            >>>     EntityTypes,
            >>>     EntityKeyTypes
            >>> )
            >>> client: CybsiClient
            >>> entities = [
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     UUID("85fca85e-0036-488d-9dcf-35970d182afc"),
            >>> ]
            >>> filter_sections = [EntityAggregateSections.AssociatedAttributes]
            >>> aggregates = client.observable.entities.aggregate(
            >>>     entities,
            >>>     sections=filter_sections
            >>> )
            >>> for item in chain_pages(aggregates):
            >>>     # Do something with an aggregate
            >>>     pass
        """
        params = {"uuid": entity_uuids}  # type: JsonObject
        if sections is not None:
            params["section"] = [section.value for section in sections]
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        r = self._connector.do_get(path=self._path, params=params)
        page = Page(self._connector.do_get, r, EntityAggregateView)
        return page

    def canonize_key(
        self, entity_type: EntityTypes, key_type: EntityKeyTypes, value: str
    ) -> EntityKeyView:
        """Get a canonized entity key.

        Note:
            Calls `GET /observable/entity-canonical-key`.
        Args:
            entity_type: Entity type.
            key_type: Key type.
            value: Key value.
        Returns:
            Canonized key view.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKey`
        Usage:
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityTypes, EntityKeyTypes
            >>> client: CybsiClient
            >>> canonized_key = client.observable.entities.canonize_key(
            >>>     EntityTypes.DomainName, EntityKeyTypes.String, "xn--80ATjc.XN--P1AI"
            >>> )
            >>> # Do something with the canonized key
            >>> print(canonized_key)
            >>> # {
            >>> #   "type": "String",
            >>> #   "value": "\u043e\u043a\u043d\u0430.\u0440\u0444"
            >>> # }
        """
        params = {
            "entityType": entity_type.value,
            "keyType": key_type.value,
            "key": value,
        }
        r = self._connector.do_get(path=self._path_canonical_key, params=params)
        return EntityKeyView(r.json())
