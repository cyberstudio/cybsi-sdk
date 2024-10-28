import uuid
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .. import RefView
from ..internal import BaseAPI, BaseAsyncAPI, rfc3339_timestamp
from ..pagination import AsyncPage, Cursor, Page
from .entity import (
    EntityAggregateView,
    EntityAttributeForecastView,
    EntityForm,
    EntityKeyView,
)
from .enums import (
    AttributeNames,
    EntityAggregateSections,
    EntityKeyTypes,
    EntityTypes,
    LinkDirection,
    RelationshipKinds,
)
from .links import EntityLinksForecastView, EntityLinkStatisticView


def _convert_attribute_name_kebab(attribute_name: AttributeNames) -> str:
    """Convert attribute name value to kebab-case.

    Args:
        attribute_name: attribute name, such of 'DomainName'.
    Return:
        Attribute name on kebab-case, such of `domain-name`.
    """
    return _attr_value_kebab_converters[attribute_name]


_attr_value_kebab_converters: Dict[AttributeNames, str] = {
    AttributeNames.Size: "size",
    AttributeNames.Class: "class",
    AttributeNames.Sectors: "sectors",
    AttributeNames.DisplayNames: "display-names",
    AttributeNames.Names: "names",
    AttributeNames.NodeRoles: "node-roles",
    AttributeNames.RelatedMalwareFamilies: "related-malware-families",
    AttributeNames.MalwareClasses: "malware-classes",
    AttributeNames.IsIoC: "is-ioc",
    AttributeNames.IsTrusted: "is-trusted",
    AttributeNames.IsDGA: "is-dga",
    AttributeNames.IsDelegated: "is-delegated",
    AttributeNames.Statuses: "statuses",
    AttributeNames.ASN: "asn",
    AttributeNames.RegionalInternetRegistry: "regional-internet-registry",
    AttributeNames.RelatedThreatCategory: "related-threat-category",
    AttributeNames.ThreatCategory: "threat-category",
    AttributeNames.MalwareNames: "malware-names",
    AttributeNames.Campaigns: "campaigns",
    AttributeNames.ThreatActors: "threat-actors",
    AttributeNames.AffectedCountries: "affected-countries",
    AttributeNames.ExploitedVulnerabilities: "exploited-vulnerabilities",
    AttributeNames.TargetedSectors: "targeted-sectors",
    AttributeNames.RegistrationCountry: "registration-country",
    AttributeNames.PotentialDamage: "potential-damage",
    AttributeNames.Platforms: "platforms",
    AttributeNames.Tactics: "tactics",
    AttributeNames.Techniques: "techniques",
    AttributeNames.Labels: "labels",
}


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
            >>> entity_form = EntityForm(
            >>>     EntityTypes.File,
            >>>     [(EntityKeyTypes.MD5, "3c4729715ef0d6bafd3d9c719e152099")],
            >>> )
            >>> # if you need to add extra key to entity form keys
            >>> entity_form.add_key(
            >>>     EntityKeyTypes.SHA1,
            >>>     "0462cb99ddd46c142aa46244cb8c2d35bfe226f5",
            >>> )
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
        *,
        sections: Optional[Iterable[EntityAggregateSections]] = None,
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

        params: Dict[str, Any] = {}
        if sections is not None:
            params["section"] = [section.value for section in sections]
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if with_valuable_facts is not None:
            params["valuableFacts"] = with_valuable_facts

        path = f"{self._path}/{entity_uuid}"
        r = self._connector.do_get(path=path, params=params)
        return EntityAggregateView(r.json())

    def aggregate(
        self,
        *,
        entity_uuids: Optional[Iterable[uuid.UUID]] = None,
        dict_item_uuid: Optional[uuid.UUID] = None,
        entity_type: Optional[EntityTypes] = None,
        key_type: Optional[EntityKeyTypes] = None,
        key: Optional[str] = None,
        suggest: Optional[str] = None,
        sections: Optional[Iterable[EntityAggregateSections]] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[EntityAggregateView]:
        """Get list of aggregated entities.

        .. versionchanged:: 2.8
            Added new parameters: `ent_type`, `key_type`, `key`.
            Parameter `entity_uuids` changed to Optional.

        .. versionchanged:: 2.11
            Added new parameter `dict_item_uuid`.

        .. versionchanged:: 2.13
            Added new parameter `suggest`.

        Note:
            Calls `GET /observable/entities`.

            To get entity aggregate, only one of [key, entity_uuids] parameters
            should be specified else Cybsi API will return error.
        Args:
            entity_uuids: Entity uuids.
                Excludes parameters: `dict_item_uuid`, `entity_type`, `key_type`, `key`,
                `suggest`.
            dict_item_uuid: Dictionary item which is attributed to the entity.
                Excludes parameters: `entity_uuids`, `entity_type`, `key_type`, `key`,
                `suggest`.
            entity_type: Entity type.
                Excludes parameter `entity_uuids`, `dict_item_uuid` and
                requires parameter `key`. The parameter is not required if
                the `entity_type` can be uniquely determined by `key_type`.
            key_type: Entity natural key type.
                Excludes parameter `entity_uuids`, `dict_item_uuid`, `suggest` and
                requires parameter `key`. The parameter is not required if
                only one `key_type` is used for the specified `entity_type`.
            key: Entity natural key value. Excludes parameter `suggest` and required
                if `entity_type` or `key_type` parameter is specified.
                It is possible to pass a key value in a non-canonical representation.
            suggest: Case-insensitive prefix of natural key or value of
                `identity.Names` attribute. Excludes parameter `key` and can be used
                with `entity_type` parameter.
                `suggest` length must greater than or equals to 2.
            sections: Sections to be aggregated.
            forecast_at: Point of time to aggregate sections at.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with aggregated entities views and next page cursor.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryItemNotFound`
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
            >>> # You can aggregate entities by entity_uuids. Be aware that
            >>> # optional parameters such as entity_type, key_type or key are excluded.
            >>> # Cybsi API will return an error if you specify
            >>> # one of these with entity_uuids.
            >>> aggregates = client.observable.entities.aggregate(
            >>>     entity_uuids=entities,
            >>>     sections=filter_sections
            >>> )
            >>> for item in chain_pages(aggregates):
            >>>     # Do something with an aggregate
            >>>     pass
            >>>
            >>> # Also you can aggregate entities by natural key, but for this
            >>> # you need to specified one of parameters entity_type or key_type.
            >>> # Keep in mind that Cybsi API will return error if you provide
            >>> # entity_uuids with natural key.
            >>> aggregates = client.observable.entities.aggregate(
            >>>     entity_type=EntityTypes.URL,
            >>>     key_type=EntityKeyTypes.String,
            >>>     key="http://young.biz/wp-content/index/",
            >>> )
        """

        params: Dict[str, Any] = {}
        if entity_uuids is not None:
            params["uuid"] = [str(u) for u in entity_uuids]
        if dict_item_uuid is not None:
            params["dictItemUUID"] = str(dict_item_uuid)
        if entity_type is not None:
            params["type"] = entity_type.value
        if key_type is not None:
            params["keyType"] = key_type.value
        if key is not None:
            params["key"] = key
        if suggest is not None:
            params["suggest"] = suggest
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

    def add_natural_keys(
        self, entity_uuid: uuid.UUID, keys: Iterable[Tuple[EntityKeyTypes, str]]
    ) -> None:
        """Add entity nalural keys.

        Note:
            Calls `PUT /observable/entities/{entity_uuid}/keys`.
        Args:
            entity_uuid: Entity UUID.
            keys: Entity natural keys.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKey`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.KeyConflict`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.BrokenKeySet`
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityKeyTypes
            >>> client: CybsiClient
            >>> entity_keys = [
            >>>     (EntityKeyTypes.MD5, "3c4729715ef0d6bafd3d9c719e152099"),
            >>>     (EntityKeyTypes.SHA1, "0462cb99ddd46c142aa46244cb8c2d35bfe226f5")
            >>> ],
            >>> client.observable.entities.add_natural_keys(
            >>>     entity_uuid=uuid.UUID("d90f5ea5-0f33-44a4-b063-6bf90e654a81"),
            >>>     form=entity_keys,
            >>> )
        """
        form = [{"type": t.value, "value": v} for t, v in keys]
        path = f"{self._path}/{entity_uuid}/keys"
        self._connector.do_put(path=path, json=form)

    def forecast_attribute_values(
        self,
        entity_uuid: uuid.UUID,
        attr_name: AttributeNames,
        forecast_at: Optional[datetime] = None,
    ) -> EntityAttributeForecastView:
        """Get a forecast of entity attribute value.

        See Also:
            See :ref:`attributes`
            for complete information about available attributes.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/attributes/{attr_name}`.
        Args:
            entity_uuid: Entity UUID.
            attr_name: Attribute name. Converts to kebab-case on URL-path.
            forecast_at: Point of time to forecast at.
                If not specified, forecast is built on current time.
        Returns:
            Attribute forecast view.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Attribute with specified name does not exist (NoSuchAttribute).
        Note:
            Semantic error codes specific for this method:
             * :attr:`~cybsi.api.error.SemanticErrorCodes.WrongEntityAttribute`
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityAttributeForecastView
            >>> from cybsi.api.observable import AttributeNames
            >>> client: CybsiClient
            >>> attr_forecast = client.observable.entities.forecast_attribute_values(
            >>>     entity_uuid=UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     attr_name=AttributeNames.IsIoC,
            >>> )
            >>> # Do something with the forecast
            >>> print(attr_forecast)
        """

        params: Dict[str, Any] = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)

        kebab_attr_name = _convert_attribute_name_kebab(attr_name)
        path = f"{self._path}/{entity_uuid}/attributes/{kebab_attr_name}"
        r = self._connector.do_get(path=path, params=params)
        return EntityAttributeForecastView(r.json(), attr_name)

    def forecast_links(
        self,
        entity_uuid: uuid.UUID,
        related_entity_types: Optional[Iterable[EntityTypes]] = None,
        direction: Optional[Iterable[LinkDirection]] = None,
        kind: Optional[Iterable[RelationshipKinds]] = None,
        confidence_threshold: Optional[float] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[EntityLinksForecastView]:
        """Get a list of link forecasts of entity.

        See Also:
            See :ref:`relationships`
            for complete information about available relationships.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/links`.
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
            Page with links forecast view and next page cursor.
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
            >>> links_forecast = client.observable.entities.forecast_links(
            >>>     entity_uuid=UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a"),
            >>>     related_entity_types=[EntityTypes.IPAddress, EntityTypes.File],
            >>>     direction=[LinkDirection.Forward],
            >>>     kind=[RelationshipKinds.ResolvesTo, RelationshipKinds.Uses],
            >>>     confidence_threshold=0.5
            >>> )
            >>> # Do something with the forecast
            >>> print(links_forecast)
        """

        params: Dict[str, Any] = {}
        if related_entity_types is not None:
            params["relatedEntityType"] = [typ.value for typ in related_entity_types]
        if direction is not None:
            params["direction"] = [d.value for d in direction]
        if kind is not None:
            params["kind"] = [k.value for k in kind]
        if confidence_threshold is not None:
            params["confidenceThreshold"] = confidence_threshold
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = f"{self._path}/{entity_uuid}/links"
        r = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, r, EntityLinksForecastView)
        return page

    def forecast_links_statistic(
        self,
        entity_uuid: uuid.UUID,
        forecast_at: Optional[datetime] = None,
    ) -> List[EntityLinkStatisticView]:
        """Get statictics of forecasted links for entity
        considering all facts about entity.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/link-type-statistic`.
        Args:
            entity_uuid: Entity UUID.
            forecast_at: Date of forecast.
                If not specified, forecast is built on current time.
        Returns:
            List of link forecasts. Links are grouped by direction, relation kind,
             and entity type. Groups are ordered by direction,
             relation kind, and entity type.
        Usage:
            >>> from uuid import UUID
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.observable import EntityLinkStatisticView
            >>> client: CybsiClient
            >>> link_forecast = client.observable.entities.forecast_links_statistic(
            >>>     entity_uuid=UUID("3a53cc35-f632-434c-bd4b-1ed8c014003a")
            >>> )
            >>> # Do something with the forecast
            >>> print(link_forecast)
        """

        params: Dict[str, Any] = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)

        path = f"{self._path}/{entity_uuid}/link-type-statistic"
        r = self._connector.do_get(path=path, params=params)
        return [EntityLinkStatisticView(v) for v in r.json()]

    def add_labels(self, entity_uuid: uuid.UUID, labels: Iterable[str]) -> None:
        """
        Add entity labels.

        .. deprecated:: 2.14 Labels are attribute of entity.
            This method will be deleted soon.
            To register labels use Generic-observation
            :meth:`~cybsi.api.observation.generic.GenericObservationsAPI.register()`.

        Note:
            Calls `PUT /observable/entities/{entityUUID}/labels`.
        Args:
            entity_uuid: Entity UUID.
            labels: List of labels. Label length must be in range [2, 50].
                Labels are converted to lowercase before saving.
        """

        path = f"{self._path}/{entity_uuid}/labels"
        self._connector.do_put(path=path, json=list(labels))

    def delete_labels(self, entity_uuid: uuid.UUID, labels: Iterable[str]) -> None:
        """Delete entity labels.

        .. deprecated:: 2.14
             Labels are attribute of entity and can't be deleted.
             This method will be deleted soon.
             Method always raises MethodNotAllowedError.

        Note:
            Calls `DELETE /observable/entities/{entityUUID}/labels`.
        Args:
            entity_uuid: Entity UUID.
            labels: List of labels.
                Labels are case-insensitive when compared.
        """

        params: Dict[str, Any] = {"label": list(labels)}
        path = f"{self._path}/{entity_uuid}/labels"
        self._connector.do_delete(path=path, params=params)


class EntitiesAsyncAPI(BaseAsyncAPI):
    """Asynchronous entities API."""

    _path = "/observable/entities"
    _path_canonical_key = "/observable/entity-canonical-key"

    async def register(self, entity: EntityForm) -> RefView:
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
            >>> import asyncio
            >>> from cybsi.api import CybsiAsyncClient
            >>> from cybsi.api.observable import EntityForm, EntityTypes, EntityKeyTypes
            >>> async def register_entities():
            >>>     entities = [
            >>>         EntityForm(
            >>>             EntityTypes.File,
            >>>             [(EntityKeyTypes.MD5, "3c4729715ef0d6bafd3d9c719e152099")]
            >>>         ),
            >>>         EntityForm(
            >>>             EntityTypes.IPAddress,
            >>>             [(EntityKeyTypes.String, "192.168.0.1")]
            >>>         ),
            >>>         EntityForm(
            >>>             EntityTypes.DomainName,
            >>>             [(EntityKeyTypes.String, "google.com")]
            >>>         ),
            >>>     ]
            >>>     # concurrently register a batch of entities
            >>>     async with CybsiAsyncClient as client:
            >>>         registrations = [
            >>>             client.observable.entities.register(e) for e in entities
            >>>         ]
            >>>         results = await asyncio.gather(*registrations)
            >>>         uuids = ", ".join(str(u.uuid) for u in results)
            >>>         print(f"Registered entities: {uuids}")
            >>> asyncio.run(register_entities())
        """
        r = await self._connector.do_put(path=self._path, json=entity.json())
        return RefView(r.json())

    async def view(
        self,
        entity_uuid: uuid.UUID,
        *,
        sections: Optional[Iterable[EntityAggregateSections]] = None,
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
        """

        params: Dict[str, Any] = {}
        if sections is not None:
            params["section"] = [section.value for section in sections]
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if with_valuable_facts is not None:
            params["valuableFacts"] = with_valuable_facts

        path = f"{self._path}/{entity_uuid}"
        r = await self._connector.do_get(path=path, params=params)
        return EntityAggregateView(r.json())

    async def aggregate(
        self,
        *,
        entity_uuids: Optional[Iterable[uuid.UUID]] = None,
        dict_item_uuid: Optional[uuid.UUID] = None,
        entity_type: Optional[EntityTypes] = None,
        key_type: Optional[EntityKeyTypes] = None,
        key: Optional[str] = None,
        suggest: Optional[str] = None,
        sections: Optional[Iterable[EntityAggregateSections]] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage[EntityAggregateView]:
        """Get list of aggregated entities.

        .. versionchanged:: 2.11
            Added new parameter `dict_item_uuid`.

        .. versionchanged:: 2.13
            Added new parameter `suggest`.

        Note:
            Calls `GET /observable/entities`.

            To get entity aggregate, only one of [key, entity_uuids] parameters
            should be specified else Cybsi API will return error.
        Args:
            entity_uuids: Entity uuids.
                Excludes parameters: `dict_item_uuid`, `entity_type`, `key_type`, `key`,
                `suggest`.
            dict_item_uuid: Dictionary item which is attributed to the entity.
                Excludes parameters: `entity_uuids`, `entity_type`, `key_type`, `key`,
                `suggest`.
            entity_type: Entity type.
                Excludes parameter `entity_uuids`, `dict_item_uuid` and
                requires parameter `key`. The parameter is not required if
                the `entity_type` can be uniquely determined by `key_type`.
            key_type: Entity natural key type.
                Excludes parameter `entity_uuids`, `dict_item_uuid`, `suggest` and
                requires parameter `key`. The parameter is not required if
                only one `key_type` is used for the specified `entity_type`.
            key: Entity natural key value. Excludes parameter `suggest` and required
                if `entity_type` or `key_type` parameter is specified.
                It is possible to pass a key value in a non-canonical representation.
            suggest: Case-insensitive prefix of natural key or value of
                `identity.Names` attribute. Excludes parameter `key` and can be used
                with `entity_type` parameter.
                `suggest` length must greater than or equals to 2.
            sections: Sections to be aggregated.
            forecast_at: Point of time to aggregate sections at.
            cursor: Page cursor.
            limit: Page limit.
        Returns:
            Page with aggregated entities views and next page cursor.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.EntityNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DictionaryItemNotFound`
        """

        params: Dict[str, Any] = {}
        if entity_uuids is not None:
            params["uuid"] = [str(u) for u in entity_uuids]
        if dict_item_uuid is not None:
            params["dictItemUUID"] = str(dict_item_uuid)
        if entity_type is not None:
            params["type"] = entity_type.value
        if key_type is not None:
            params["keyType"] = key_type.value
        if key is not None:
            params["key"] = key
        if suggest is not None:
            params["suggest"] = suggest
        if sections is not None:
            params["section"] = [section.value for section in sections]
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = limit

        r = await self._connector.do_get(path=self._path, params=params)
        page = AsyncPage(self._connector.do_get, r, EntityAggregateView)
        return page

    async def canonize_key(
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
        """
        params = {
            "entityType": entity_type.value,
            "keyType": key_type.value,
            "key": value,
        }
        r = await self._connector.do_get(path=self._path_canonical_key, params=params)
        return EntityKeyView(r.json())

    async def add_natural_keys(
        self, entity_uuid: uuid.UUID, keys: Iterable[Tuple[EntityKeyTypes, str]]
    ) -> None:
        """Add entity nalural keys.

        Note:
            Calls `PUT /observable/entities/{entity_uuid}/keys`.
        Args:
            entity_uuid: Entity UUID.
            keys: Entity natural keys.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKey`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.KeyConflict`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.BrokenKeySet`
        """
        form = [{"type": t.value, "value": v} for t, v in keys]
        path = f"{self._path}/{entity_uuid}/keys"
        await self._connector.do_put(path=path, json=form)

    async def forecast_attribute_values(
        self,
        entity_uuid: uuid.UUID,
        attr_name: AttributeNames,
        forecast_at: Optional[datetime] = None,
    ) -> EntityAttributeForecastView:
        """Get a forecast of entity attribute value.

        See Also:
            See :ref:`attributes`
            for complete information about available attributes.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/attributes/{attr_name}`.
        Args:
            entity_uuid: Entity UUID.
            attr_name: Attribute name. Converts to kebab-case on URL-path.
            forecast_at: Point of time to forecast at.
                If not specified, forecast is built on current time.
        Returns:
            Attribute forecast view.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Query contains logic errors.
            :class:`~cybsi.api.error.InvalidRequestError`:
                Attribute with specified name does not exist (NoSuchAttribute).
        Note:
            Semantic error codes specific for this method:
             * :attr:`~cybsi.api.error.SemanticErrorCodes.WrongEntityAttribute`
        """

        params: Dict[str, Any] = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)

        kebab_attr_name = _convert_attribute_name_kebab(attr_name)
        path = f"{self._path}/{entity_uuid}/attributes/{kebab_attr_name}"
        r = await self._connector.do_get(path=path, params=params)
        return EntityAttributeForecastView(r.json(), attr_name)

    async def forecast_links(
        self,
        entity_uuid: uuid.UUID,
        related_entity_types: Optional[Iterable[EntityTypes]] = None,
        direction: Optional[Iterable[LinkDirection]] = None,
        kind: Optional[Iterable[RelationshipKinds]] = None,
        confidence_threshold: Optional[float] = None,
        forecast_at: Optional[datetime] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> AsyncPage[EntityLinksForecastView]:
        """Get a list of link forecasts of entity.

        See Also:
            See :ref:`relationships`
            for complete information about available relationships.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/links`.
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
            Page with links forecast view and next page cursor.
        """

        params: Dict[str, Any] = {}
        if related_entity_types is not None:
            params["relatedEntityType"] = [typ.value for typ in related_entity_types]
        if direction is not None:
            params["direction"] = [d.value for d in direction]
        if kind is not None:
            params["kind"] = [k.value for k in kind]
        if confidence_threshold is not None:
            params["confidenceThreshold"] = confidence_threshold
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        path = f"{self._path}/{entity_uuid}/links"
        r = await self._connector.do_get(path=path, params=params)
        page = AsyncPage(self._connector.do_get, r, EntityLinksForecastView)
        return page

    async def forecast_links_statistic(
        self,
        entity_uuid: uuid.UUID,
        forecast_at: Optional[datetime] = None,
    ) -> List[EntityLinkStatisticView]:
        """Get statictics of forecasted links for entity
        considering all facts about entity.

        Note:
            Calls `GET /observable/entities/{entity_uuid}/link-type-statistic`.
        Args:
            entity_uuid: Entity UUID.
            forecast_at: Date of forecast.
                If not specified, forecast is built on current time.
        Returns:
            List of link forecasts. Links are grouped by direction, relation kind,
             and entity type. Groups are ordered by direction,
             relation kind, and entity type.
        """

        params: Dict[str, Any] = {}
        if forecast_at is not None:
            params["forecastAt"] = rfc3339_timestamp(forecast_at)

        path = f"{self._path}/{entity_uuid}/link-type-statistic"
        r = await self._connector.do_get(path=path, params=params)
        return [EntityLinkStatisticView(v) for v in r.json()]

    async def add_labels(self, entity_uuid: uuid.UUID, labels: Iterable[str]) -> None:
        """
        Add entity labels.

        .. deprecated:: 2.14 Labels are attribute of entity.
             This method will be deleted soon.
             To register labels use Generic-observation
             :meth:`~cybsi.api.observation.generic.GenericObservationsAsyncAPI.register()`.

        Note:
            Calls `PUT /observable/entities/{entityUUID}/labels`.
        Args:
            entity_uuid: Entity UUID.
            labels: List of labels. Label length must be in range [2, 50].
                Labels are converted to lowercase before saving.
        """

        path = f"{self._path}/{entity_uuid}/labels"
        await self._connector.do_put(path=path, json=list(labels))

    async def delete_labels(
        self, entity_uuid: uuid.UUID, labels: Iterable[str]
    ) -> None:
        """Delete entity labels.

        .. deprecated:: 2.14
             Labels are attribute of entity and can't be deleted.
             This method will be deleted soon.
             Method always raises MethodNotAllowedError.

        Note:
            Calls `DELETE /observable/entities/{entityUUID}/labels`.
        Args:
            entity_uuid: Entity UUID.
            labels: List of labels.
                Labels are case-insensitive when compared.
        """

        params: Dict[str, Any] = {"label": list(labels)}
        path = f"{self._path}/{entity_uuid}/labels"
        await self._connector.do_delete(path=path, params=params)
