import uuid
from datetime import datetime
from typing import Optional, List

from cybsi.api.error import JsonObject
from cybsi.utils.converters import convert_attribute_name_kebab

from .entity import (
    EntityAttributeForecastView,
    EntityForm,
    EntityAggregateView,
    EntityKeyView,
)

from .enums import (
    AttributeNames,
    EntityTypes,
    EntityAggregateSections,
    EntityKeyTypes,
    LinkDirection,
    RelationshipKinds,
)
from .links import EntityLinksForecastView, EntityLinkStatisticView

from .. import RefView
from ..internal import BaseAPI, rfc3339_timestamp
from ..pagination import Page, Cursor


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
            Calls `GET /observable/entities/{entity_uuid}`.
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
        cursor: Optional[Cursor] = None,
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
            params["cursor"] = str(cursor)
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

    def forecast_attribute_values(
        self,
        entity_uuid: uuid.UUID,
        attr_name: AttributeNames,
        forecast_at: Optional[datetime] = None,
    ) -> EntityAttributeForecastView:
        """Get a forecast of entity attribute value.

        Note:
            Calls `GET /observable/entities/{entityUUID}/attributes/{attributeName}`.
        Args:
            entity_uuid: Entity UUID.
            attr_name: Attribute name. Converts to kebab-case on URL-path.
            forecast_at: Point of time to forecast at.
                If not specified, forecast is built on current time.
        Returns:
            Attribute forecast view.
        Raises:
              * :attr:`~cybsi.api.error.InvalidRequestError.NoSuchAttribute`:
                Attribute with specified name does not exist.
              * :attr:`~cybsi.api.error.SemanticErrorCodes.WrongEntityAttribute`:
                Attribute is not registered for entity with given UUID.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityAttributeForecastView
            >>> from cybsi.api.observable import AttributeNames
            >>> client: CybsiClient
            >>> forecast = client.observable.entities.forecast_attribute_values(
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     AttributeNames.IsMalicious,
            >>> )
            >>> # Do something with the forecast
            >>> print(forecast)
        """
        kebab_attr_name = convert_attribute_name_kebab(attr_name)
        path = f"{self._path}/{entity_uuid}/attributes/{kebab_attr_name}"
        params = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        r = self._connector.do_get(path=path, params=params)
        return EntityAttributeForecastView(r.json())

    def forecast_links(
        self,
        entity_uuid: uuid.UUID,
        related_entity_types: Optional[List[EntityTypes]] = None,
        direction: Optional[List[LinkDirection]] = None,
        kind: Optional[List[RelationshipKinds]] = None,
        confidence_threshold: Optional[float] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Page[EntityLinksForecastView]:
        """Get a list of link forecasts of entity.

        Note:
            Calls `GET /observable/entities/{entityUUID}/links`.
        Args:
            entity_uuid: Entity UUID.
            related_entity_types: Related entity types.
            direction: Link direction. Return any if not specified.
            kind: Kind of relationship. Return any if not specified.
            confidence_threshold: Discard links with confidence
                less than threshold. Valid values are in (0, 1].
            forecast_at: Date of forecast.
                If not specified, forecast is built on current time.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with links forecast view.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>> from cybsi.api.observable import (
            >>>     EntityTypes,
            >>>     LinkDirection,
            >>>     RelationshipKinds,
            >>> )
            >>> from cybsi.api.observable import EntityLinksForecastView
            >>> client: CybsiClient
            >>> forecasts = client.observable.entities.forecast_links(
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     related_entity_types = [EntityTypes.IPAddress, EntityTypes.File]
            >>>     direction = [LinkDirection.Forward],
            >>>     kind = [RelationshipKind.ResolvesTo, RelationshipKind.Uses],
            >>>     confidence_threshold = 0.5,
            >>> )
            >>> # Do something with the forecast
            >>> print(forecast)
        """
        path = f"{self._path}/{entity_uuid}/links"
        params = {}  # type: JsonObject
        if related_entity_types is not None:
            params["relatedEntityType"] = [typ.value for typ in related_entity_types]
        if direction is not None:
            params["direction"] = [dir.value for dir in direction]
        if kind is not None:
            params["kind"] = [k.value for k in kind]
        if confidence_threshold is not None:
            params["confidenceThreshold"] = confidence_threshold
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if cursor:
            params["cursor"] = cursor
        if limit:
            params["limit"] = limit
        r = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, r, EntityLinksForecastView)
        return page

    def forecast_links_statistic(
        self,
        entity_uuid: uuid.UUID,
        forecast_at: Optional[datetime] = None,
    ) -> EntityLinkStatisticView:
        """Get statictics of links for entity.

        Note:
            Calls `GET /observable/entities/{entityUUID}/link-type-statistic`.
        Args:
            entity_uuid: Entity UUID.
            forecast_at: Date of forecast.
                If not specified, forecast is built on current time.
        Returns:
            Link types statistic forecast view.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityLinkStatisticView
            >>> client: CybsiClient
            >>> forecasts = client.observable.entities.forecast_links_statistic(
            >>>     UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a")
            >>> )
            >>> # Do something with the forecast
            >>> print(forecast)
        """
        path = f"{self._path}/{entity_uuid}/link-type-statistic"
        params = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        r = self._connector.do_get(path=path, params=params)
        return EntityLinkStatisticView(r.json())
