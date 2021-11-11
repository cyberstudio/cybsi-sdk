"""Generic observation is the main form of observation.
In essence, it's a container of arbitrary facts Cybsi domain model supports.

See Also:
    See :ref:`register-generic-observation-example`
    for a complete example of generic observation API usage.
"""
import datetime
import uuid

from typing import Any, cast, List, Optional

from ..common import RefView
from ..internal import (
    BaseAPI,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
    rfc3339_timestamp,
)
from ..observable import (
    AttributeNames,
    EntityForm,
    EntityView,
    RelationshipKinds,
    ShareLevels,
)


class GenericObservationsAPI(BaseAPI):
    """Generic observation API."""

    _path = "/enrichment/observations/generics"

    def register(self, observation: "GenericObservationForm") -> RefView:
        """Register a generic observation.

        Note:
            Calls `POST /enrichment/observations/generics`.
        Args:
            observation: Filled generic observation form.
        Returns:
            Reference to a newly registered observation.
        """
        r = self._connector.do_post(path=self._path, json=observation.json())
        return RefView(r.json())

    def view(self, observation_uuid: uuid.UUID) -> "GenericObservationView":
        """Get a generic observation view.

        Note:
            Calls `GET /enrichment/observations/generics`.

        Args:
            observation_uuid: Observation uuid.
        Returns:
            View of the observation.
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
        >>>     EntityKeyTypes, EntityTypes, ShareLevels
        >>> )
        >>> from cybsi.api.observation import GenericObservationForm
        >>> domain = EntityForm(EntityTypes.DomainName)
        >>> domain.add_key(EntityKeyTypes.String, "test.com")
        >>> observation = GenericObservationForm(
        >>>    share_level=ShareLevels.Green,
        >>>    seen_at=datetime.now(timezone.utc)
        >>> ).add_attribute_fact(
        >>>     entity=domain,
        >>>     attribute_name=AttributeNames.IsIoC,
        >>>     value=True,
        >>>     confidence=0.9
        >>> )
    """

    def __init__(self, share_level: ShareLevels, seen_at: datetime.datetime):
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
        entity: EntityForm,
        attribute_name: AttributeNames,
        value: Any,
        confidence: Optional[float] = None,
    ) -> "GenericObservationForm":
        """Add attribute value fact to the observation.

        Args:
            entity: Filled form of entity.
            attribute_name: Attribute name.
            value: Attribute value.
            confidence: Fact confidence.
        Return:
            Updated observation form.
        """
        attribute_facts = self._content.setdefault("entityAttributeValues", [])
        attribute_facts.append(
            {
                "entity": entity.json(),
                "attributeName": attribute_name.value,
                "value": value,
                "confidence": confidence,
            }
        )
        return self

    def add_entity_relationship(
        self,
        source: EntityForm,
        kind: RelationshipKinds,
        target: EntityForm,
        confidence: Optional[float] = None,
    ) -> "GenericObservationForm":
        """Add entity relationship to observation.

        Args:
            source: Filled form of source entity in the relationship.
            kind: Kind of relationship.
            target: Filled form of target entity in the relationship.
            confidence: Relationship confidence.
        Returns:
            Updated observation form.
        Warning:
            Not implemented yet.
        """
        raise NotImplementedError()


class GenericObservationView(JsonObjectView):
    """View of a generic observation,
    as retrieved by :meth:`GenericObservationAPI.view`."""

    @property
    def reporter(self) -> RefView:
        """Reporter."""

        return RefView(self._get("reporter"))

    @property
    def data_source(self) -> RefView:
        """Data source."""

        return RefView(self._get("dataSource"))

    @property
    def share_level(self) -> ShareLevels:
        """Share level."""

        return ShareLevels(self._get("shareLevel"))

    @property
    def seen_at(self) -> datetime.datetime:
        """Date and time when observation was seen."""

        return parse_rfc3339_timestamp(self._get("seenAt"))

    @property
    def registered_at(self) -> datetime.datetime:
        """Date and time when observation was registered."""

        return parse_rfc3339_timestamp(self._get("registeredAt"))

    @property
    def content(self) -> "GenericObservationContentView":
        """Content."""

        return GenericObservationContentView(self._get("content"))


class GenericObservationContentView(dict):
    """Generic observation content."""

    @property
    def entity_relationships(self) -> List["RelationshipView"]:
        """Entity relationships."""

        relationships = self.get("entityRelationships", [])
        return [RelationshipView(x) for x in relationships]

    @property
    def entity_attribute_values(self) -> List["AttributeValueView"]:
        """Entity attribute values."""

        attributes = self.get("entityAttributeValues", [])
        return [AttributeValueView(x) for x in attributes]


class RelationshipView(dict):
    """Relationship fact view."""

    @property
    def source(self) -> EntityView:
        """Relationship's source entity.

        Warning:
            Ref uuid may be zero uuid,
            if source entity keys were invalid during registration.
        """

        return EntityView(self.get("source"))

    @property
    def kind(self) -> RelationshipKinds:
        """Kind of the relationship."""

        return RelationshipKinds(self.get("kind"))

    @property
    def target(self) -> EntityView:
        """Target entity.

        Warning:
            Ref uuid may be zero uuid,
            if source entity keys were invalid during registration.
        """

        return EntityView(self.get("target"))

    @property
    def confidence(self) -> float:
        """Relationship fact confidence."""

        return float(cast(float, self.get("confidence")))


class AttributeValueView(dict):
    """Attribute value fact view."""

    @property
    def entity(self) -> EntityView:
        """Entity of the fact.

        Warning:
            Ref uuid may be zero uuid,
            if entity keys were invalid during registration.
        """

        return EntityView(self.get("entity"))

    @property
    def attribute_name(self) -> AttributeNames:
        """Attribute name."""

        return AttributeNames(self.get("attributeName"))

    @property
    def value(self) -> Any:
        """Value of the attribute.

        Return type depends on attribute name and entity type.
        """

        return self.get("value")

    @property
    def confidence(self) -> float:
        """Fact confidence."""

        return float(cast(float, self.get("confidence")))
