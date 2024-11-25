import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

from .. import RefView
from ..dictionary import DictionaryItemCommonView
from ..internal import JsonObject, JsonObjectView, list_mapper, parse_rfc3339_timestamp
from .enums import (
    AttributeNames,
    EntityAggregateSections,
    IdentityClass,
    NodeRole,
    PotentialDamage,
    RelatedThreatCategory,
    ShareLevels,
    ThreatCategory,
    ThreatStatus,
    RegionalInternetRegistry,
)

T = TypeVar("T")
"""Type of section data. Depends on section name."""

AttributeValueView = Union[str, bool, int, uuid.UUID, DictionaryItemCommonView, Enum]


def _convert_attribute_value_type(
    attribute_name: AttributeNames, val: Any
) -> AttributeValueView:
    _attribute_value_types = {
        AttributeNames.Names: str,
        AttributeNames.DisplayNames: str,
        AttributeNames.IsIoC: bool,
        AttributeNames.IsDGA: bool,
        AttributeNames.IsTrusted: bool,
        AttributeNames.Size: int,
        AttributeNames.MalwareNames: str,
        AttributeNames.MalwareClasses: DictionaryItemCommonView,
        AttributeNames.MalwareFamilies: DictionaryItemCommonView,
        AttributeNames.RelatedMalwareFamilies: DictionaryItemCommonView,
        AttributeNames.NodeRoles: NodeRole,
        AttributeNames.ThreatCategory: ThreatCategory,
        AttributeNames.RelatedThreatCategory: RelatedThreatCategory,
        AttributeNames.Sectors: DictionaryItemCommonView,
        AttributeNames.Class: IdentityClass,
        AttributeNames.ASN: int,
        AttributeNames.Statuses: DictionaryItemCommonView,
        AttributeNames.Campaigns: DictionaryItemCommonView,
        AttributeNames.ThreatActors: DictionaryItemCommonView,
        AttributeNames.AffectedCountries: DictionaryItemCommonView,
        AttributeNames.ExploitedVulnerabilities: DictionaryItemCommonView,
        AttributeNames.TargetedSectors: DictionaryItemCommonView,
        AttributeNames.RegistrationCountry: DictionaryItemCommonView,
        AttributeNames.PotentialDamage: PotentialDamage,
        AttributeNames.Platforms: DictionaryItemCommonView,
        AttributeNames.Tactics: DictionaryItemCommonView,
        AttributeNames.Techniques: DictionaryItemCommonView,
        AttributeNames.Labels: DictionaryItemCommonView,
        AttributeNames.IsDelegated: bool,
        AttributeNames.RegionalInternetRegistry: RegionalInternetRegistry
    }

    return _attribute_value_types[attribute_name](val)


class SectionView(JsonObjectView, Generic[T]):
    """Common section view."""

    def __init__(self, data: JsonObject, data_view: Callable[..., T]):
        super().__init__(data)
        self._data_view = data_view

    @property
    def name(self) -> str:
        """Section name."""
        return self._get("name")

    @property
    def data_raw(self) -> Any:
        """Section raw data."""
        return self._get("data")

    @property
    def data(self) -> T:
        """Section data."""
        return self._data_view(self._get("data"))


class ValuableFactView(JsonObjectView):
    """Facts influenced on value and its confidence."""

    @property
    def data_source(self) -> RefView:
        """Data source of the fact."""
        return RefView(self._get("dataSource"))

    @property
    def share_level(self) -> ShareLevels:
        """Share level of the fact."""
        return ShareLevels(self._get("shareLevel"))

    @property
    def seen_at(self) -> datetime:
        """Date and time when facts were seen."""
        return parse_rfc3339_timestamp(self._get("seenAt"))

    @property
    def confidence(self) -> float:
        """Data source confidence in the fact.
        Value is in range (0; 1]."""
        return self._get("confidence")

    @property
    def final_confidence(self) -> float:
        """Cybsi final confidence in the fact.
        Value is in range (0; 1]."""
        return self._get("finalConfidence")


class AttributeValuableFactView(ValuableFactView):
    """Valuable fact of attribute forecast view."""

    def __init__(self, data: JsonObject, attribute_name: AttributeNames):
        super().__init__(data)
        self._attribute_name = attribute_name

    @property
    def value(self) -> "AttributeValueView":
        """Facts attribute value. Returned value type depends on attribute.

        Usage:
            >>> from typing import cast
            >>> from cybsi.api.observable import AttributeValuableFactView
            >>> from cybsi.api.dictionary import DictionaryItemCommonView
            >>>
            >>> view = AttributesSectionData()
            >>> if view.attribute_name == AttributeNames.MalwareFamilies:
            >>>     for v in view.values:
            >>>         value = cast(DictionaryItemCommonView, v.value)
            >>>         print(value)
        """
        return _convert_attribute_value_type(self._attribute_name, self._get("value"))


class AttributeAggregatedValue(JsonObjectView):
    """View for attribute value aggregated data."""

    def __init__(self, data: JsonObject, attribute_name: AttributeNames):
        super().__init__(data)
        self._attribute_name = attribute_name

    @property
    def value(self) -> "AttributeValueView":
        """Attribute value. Returned value type depends on attribute.

        Usage:
            >>> from typing import cast
            >>> from cybsi.api.observable import AttributeValuableFactView
            >>> from cybsi.api.dictionary import DictionaryItemCommonView
            >>>
            >>> view = AttributesSectionData()
            >>> if view.attribute_name == AttributeNames.MalwareFamilies:
            >>>     for v in view.values:
            >>>         value = cast(DictionaryItemCommonView, v.value)
            >>>         print(value)
        """
        return _convert_attribute_value_type(self._attribute_name, self._get("value"))

    @property
    def confidence(self) -> float:
        """Confidence of the value. Value is in range (0; 1]."""
        return self._get("confidence")

    @property
    def valuable_facts(self) -> Optional[List[AttributeValuableFactView]]:
        """Facts influenced on value and its confidence.
        Can return None if valuable facts list is not set.

        Note:
            This list is not set in common aggregate methods results.
        """
        facts = self._get("valuableFacts")
        return (
            [AttributeValuableFactView(fact, self._attribute_name) for fact in facts]
            if facts is not None
            else None
        )


class AttributesSectionData(JsonObjectView):
    """View for attributes section data."""

    @property
    def attribute_name(self) -> AttributeNames:
        """Attribute name."""
        return AttributeNames(self._get("attributeName"))

    @property
    def has_conflicts(self) -> bool:
        """Attribute value has conflicts."""
        return self._get("hasConflicts")

    @property
    def values(self) -> List[AttributeAggregatedValue]:
        """Attribute values."""
        return [
            AttributeAggregatedValue(value, self.attribute_name)
            for value in self._get("values")
        ]


class ThreatSectionData(JsonObjectView):
    """View for threat section data."""

    @property
    def status(self) -> ThreatStatus:
        """Threat status."""
        return ThreatStatus(self._get("status"))


class GeoIPSectionData(JsonObjectView):
    """View for GeoIP section data."""

    @property
    def asn(self) -> Optional[int]:
        """Autonomous system number."""
        return self._get("asn")

    @property
    def country_code(self) -> Optional[str]:
        """Country cody in ISO."""
        return self._get("countryCode")

    @property
    def country(self) -> Optional[str]:
        """Country name."""
        return self._get("country")


class LabelsSectionData(JsonObjectView):
    """View for labels section data."""

    @property
    def labels(self) -> List[str]:
        """Labels."""
        return self._get("labels")


class SectionsView:
    """Sections list view."""

    _section_converters = {
        EntityAggregateSections.AssociatedAttributes: list_mapper(
            AttributesSectionData
        ),
        EntityAggregateSections.NaturalAttributes: list_mapper(AttributesSectionData),
        EntityAggregateSections.Threat: ThreatSectionData,
        EntityAggregateSections.GeoIP: GeoIPSectionData,
        EntityAggregateSections.Labels: LabelsSectionData,
    }

    def __init__(self, data: List[JsonObject]):
        self._sections: Dict[EntityAggregateSections, Any] = {}
        for section in data:
            section_name = EntityAggregateSections(section["name"])
            view: Any = SectionView(
                section, self._section_converters[section_name]  # type: ignore
            )
            self._sections[section_name] = view

    @property
    def associated_attributes(self) -> SectionView[List[AttributesSectionData]]:
        """Associated with the entity attributes.

        Raises:
            :class:`KeyError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        val = self._sections[EntityAggregateSections.AssociatedAttributes]
        return val  # type: ignore

    @property
    def natural_attributes(self) -> SectionView[List[AttributesSectionData]]:
        """Natural attributes of the entity.

        Raises:
            :class:`KeyError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        val = self._sections[EntityAggregateSections.NaturalAttributes]
        return val  # type: ignore

    @property
    def threat(self) -> SectionView[ThreatSectionData]:
        """Entity threat status.

        Raises:
            :class:`KeyError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.Threat]  # type: ignore

    @property
    def geo_ip(self) -> SectionView[GeoIPSectionData]:
        """GeoIP information.

        Raises:
            :class:`KeyError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.GeoIP]  # type: ignore

    @property
    def labels(self) -> SectionView[LabelsSectionData]:
        """Labels of the entity.

        Raises:
            :class:`KeyError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.Labels]  # type: ignore
