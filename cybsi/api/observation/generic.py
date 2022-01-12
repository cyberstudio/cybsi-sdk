"""Generic observation is the main form of observation.
In essence, it's a container of arbitrary facts Cybsi domain model supports.

See Also:
    See :ref:`register-generic-observation-example`
    for a complete example of generic observation API usage.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union, cast

from .. import RefView
from ..internal import BaseAPI, JsonObjectForm, JsonObjectView, rfc3339_timestamp
from ..observable import (
    AttributeNames,
    EntityForm,
    EntityView,
    RelationshipKinds,
    RelationshipView,
    ShareLevels,
)
from ..pagination import Cursor, Page
from .view import ObservationHeaderView


class GenericObservationsAPI(BaseAPI):
    """Generic observation API."""

    _path = "/enrichment/observations/generics"

    def register(self, observation: "GenericObservationForm") -> RefView:
        """Register a generic observation.

        The observation is always registered unless it contains logic errors.
        Entity key value validation errors are ignored.

        Note:
            Calls `POST /enrichment/observations/generics`.
        Args:
            observation: Filled generic observation form.
        Returns:
            Reference to a newly registered observation.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DuplicatedEntityAttribute`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidAttribute`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidAttributeValue`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidKeySet`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidRelationship`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidShareLevel`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.InvalidTime`
        """
        r = self._connector.do_post(path=self._path, json=observation.json())
        return RefView(r.json())

    def filter(
        self,
        data_source_uuids: Optional[List[uuid.UUID]] = None,
        reporter_uuids: Optional[List[uuid.UUID]] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["GenericObservationView"]:
        """Get page of filtered generic observation list.

        Page's items are sorted in descending order of observation time.

        Note:
            Calls `GET /enrichment/observations/generics`
        Args:
            cursor: Page cursor.
            limit: Page limit.
            data_source_uuids: List of data source identifiers.
                Filter observations by original data source identifiers.
            reporter_uuids: List of reporter identifiers.
                Filter observations by reporter data source identifiers.
        Returns:
            Page of generic observations list and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """
        params: Dict[str, Any] = {}

        if data_source_uuids is not None:
            params["dataSourceUUID"] = [str(u) for u in data_source_uuids]
        if reporter_uuids is not None:
            params["reporterUUID"] = [str(u) for u in reporter_uuids]
        if cursor:
            params["cursor"] = str(cursor)
        if limit:
            params["limit"] = str(limit)

        resp = self._connector.do_get(self._path, params=params)
        page = Page(self._connector.do_get, resp, GenericObservationView)
        return page

    def view(self, observation_uuid: uuid.UUID) -> "GenericObservationView":
        """Get the generic observation view.

        Note:
            Calls `GET /enrichment/observations/generics/{observation_uuid}`.
        Args:
            observation_uuid: Observation uuid.
        Returns:
            View of the observation.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Generic observation not found.
        """
        path = f"{self._path}/{observation_uuid}"
        r = self._connector.do_get(path)
        return GenericObservationView(r.json())


class GenericObservationForm(JsonObjectForm):
    """Generic observation form.

    This is the form you need to fill to register observation.
    To fill the form, call :meth:`add_attribute_fact`
    and :meth:`add_entity_relationship`
    for each fact and relationship you observe.

    Args:
        share_level: Share level of the observation.
        seen_at: Date and time when facts were seen.
    Usage:
        >>> from datetime import datetime, timezone
        >>> from cybsi.api.observable import (
        >>>     AttributeNames, EntityForm,
        >>>     EntityKeyTypes, EntityTypes,
        >>>     ShareLevels, RelationshipKinds
        >>> )
        >>> from cybsi.api.observation import GenericObservationForm
        >>> domain = EntityForm(EntityTypes.DomainName)
        >>> domain.add_key(EntityKeyTypes.String, "test.com")
        >>> ip_address = EntityForm(EntityTypes.IPAddress)
        >>> ip_address.add_key(EntityKeyTypes.String, "8.8.8.8")
        >>> observation = GenericObservationForm(
        >>>    share_level=ShareLevels.Green,
        >>>    seen_at=datetime.now(timezone.utc)
        >>> ).add_attribute_fact(
        >>>     entity=domain,
        >>>     attribute_name=AttributeNames.IsIoC,
        >>>     value=True,
        >>>     confidence=0.9
        >>> ).add_entity_relationship(
        >>>     source=domain,
        >>>     kind=RelationshipKinds.Resolves,
        >>>     target=ip_address,
        >>>     confidence=0.5,
        >>>)
    """

    def __init__(self, share_level: ShareLevels, seen_at: datetime):
        super().__init__()
        self._data["shareLevel"] = share_level.value
        self._data["seenAt"] = rfc3339_timestamp(seen_at)

    @property
    def _content(self):
        return self._data.setdefault("content", {})

    def set_data_source(self, source_uuid: uuid.UUID):
        """Set observation data source."""

        self._data["dataSourceUUID"] = str(source_uuid)
        return self

    def add_attribute_fact(
        self,
        entity: Union[uuid.UUID, EntityForm],
        attribute_name: AttributeNames,
        value: Any,
        confidence: Optional[float] = None,
    ) -> "GenericObservationForm":
        """Add attribute value fact to the observation.

        Args:
            entity: Filled form of entity or passed uuid of entity.
                Entity with passed UUID must be registered in system.
            attribute_name: Attribute name.
            value: Attribute value. Type depends on attribute name and entity type.
            confidence: Fact confidence. Confidence must be in range (0;1].
                Empty value means default value (1)
        Return:
            Updated observation form.
        """
        attribute_facts = self._content.setdefault("entityAttributeValues", [])

        if isinstance(entity, uuid.UUID):
            ent = {"uuid": str(entity)}
        else:
            ent = entity.json()

        attribute_facts.append(
            {
                "entity": ent,
                "attributeName": attribute_name.value,
                "value": value,
                "confidence": confidence,
            }
        )
        return self

    def add_entity_relationship(
        self,
        source: Union[uuid.UUID, EntityForm],
        kind: RelationshipKinds,
        target: Union[uuid.UUID, EntityForm],
        confidence: Optional[float] = None,
    ) -> "GenericObservationForm":
        """Add entity relationship to observation.

        Args:
            source: Filled form of source entity in the relationship or
                passed uuid of source entity.
                Entity with passed UUID must be registered in system.
            kind: Kind of relationship.
            target: Filled form of target entity in the relationship or
                passed uuid of target entity.
                Entity with passed UUID must be registered in system.
            confidence: Relationship confidence. Confidence must be in range (0;1].
                Empty value means default value (1)
        Returns:
            Updated observation form.
        """
        entity_relationship = self._content.setdefault("entityRelationships", [])

        if isinstance(source, uuid.UUID):
            source_ent = {"uuid": str(source)}
        else:
            source_ent = source.json()

        if isinstance(target, uuid.UUID):
            target_ent = {"uuid": str(target)}
        else:
            target_ent = target.json()

        entity_relationship.append(
            {
                "source": source_ent,
                "kind": kind.value,
                "target": target_ent,
                "confidence": confidence,
            }
        )
        return self


class GenericObservationView(ObservationHeaderView):
    """Generic observation view,
    as retrieved by :meth:`GenericObservationsAPI.view`."""

    @property
    def content(self) -> "GenericObservationContentView":
        """Content."""

        return GenericObservationContentView(self._get("content"))


class GenericObservationContentView(JsonObjectView):
    """Generic observation content."""

    @property
    def entity_relationships(self) -> List["RelationshipView"]:
        """Entity relationships."""

        relationships = self._get("entityRelationships")
        return [RelationshipView(x) for x in relationships]

    @property
    def entity_attribute_values(self) -> List["AttributeValueView"]:
        """Entity attribute values."""

        attributes = self._get("entityAttributeValues")
        return [AttributeValueView(x) for x in attributes]


class AttributeValueView(JsonObjectView):
    """Attribute value fact view."""

    @property
    def entity(self) -> EntityView:
        """Entity of the fact.

        Warning:
            Ref uuid may be zero uuid,
            if entity keys were invalid during registration.
        """

        return EntityView(self._get("entity"))

    @property
    def attribute_name(self) -> AttributeNames:
        """Attribute name."""

        return AttributeNames(self._get("attributeName"))

    @property
    def value(self) -> Any:
        """Value of the attribute.

        Return type depends on attribute name and entity type.
        """

        return self._get("value")

    @property
    def confidence(self) -> float:
        """Fact confidence."""

        return float(cast(float, self._get("confidence")))
