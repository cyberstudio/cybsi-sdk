from datetime import datetime
from typing import Any, List, TypeVar, Generic, Callable, Optional
from typing import Dict

from .. import RefView
from ..internal import JsonObject, JsonObjectView, list_mapper, parse_rfc3339_timestamp

from .enums import EntityAggregateSections, ThreatStatus, ShareLevels

T = TypeVar("T")


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


class AttributeValuableFact(JsonObjectView):
    """Facts influenced on value and its confidence."""

    @property
    def data_source(self) -> RefView:
        """DataSource of the fact."""
        return RefView(self._get("dataSource"))

    @property
    def share_level(self) -> ShareLevels:
        """ShareLevel of the fact."""
        return ShareLevels(self._get("shareLevel"))

    @property
    def seen_at(self) -> datetime:
        """ShareLevel of the fact."""
        return parse_rfc3339_timestamp(self._get("seenAt"))

    @property
    def confidence(self) -> float:
        """DataSource confidence in the fact.
        Value is in range (0; 1]."""
        return self._get("confidence")

    @property
    def final_confidence(self) -> float:
        """Cybsi final confidence in the fact.
        Value is in range (0; 1]."""
        return self._get("finalConfidence")

    @property
    def value(self) -> Any:
        """Fact value."""
        return self._get("value")


class AttributeAggregatedValue(JsonObjectView):
    """View for attribute value aggregated data."""

    @property
    def value(self) -> Any:
        """Attribute value."""
        return self._get("value")

    @property
    def confidence(self) -> float:
        """Confidence of the value. Value is in range (0; 1]."""
        return self._get("confidence")

    @property
    def valuable_facts(self) -> Optional[List[AttributeValuableFact]]:
        """Facts influenced on value and its confidence.
        Can return None if valuable facts list is not set.

        Note:
            This list is not set in common aggregate methods results.
        """
        facts = self._get("valuableFacts")
        return (
            [AttributeValuableFact(fact) for fact in facts]
            if facts is not None
            else None
        )


class AttributesSectionData(JsonObjectView):
    """View for attributes section data."""

    @property
    def attribute_name(self) -> str:
        """Attribute name."""
        return self._get("attributeName")

    @property
    def has_conflicts(self) -> bool:
        """Attribute value has conflicts."""
        return self._get("hasConflicts")

    @property
    def values(self) -> List[AttributeAggregatedValue]:
        """Attribute values."""
        return [AttributeAggregatedValue(value) for value in self._get("values")]


class ThreatSectionData(JsonObjectView):
    """View for threat section data."""

    @property
    def status(self) -> ThreatStatus:
        """Threat status."""
        return ThreatStatus(self._get("status"))


class AVScanStatisticsSectionData(JsonObjectView):
    """View for AVScanStatistics section data."""

    @property
    def malware_name(self) -> Optional[str]:
        """Malware name."""
        return self._get("malwareName")


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
        EntityAggregateSections.AVScanStatistics: AVScanStatisticsSectionData,
        EntityAggregateSections.GeoIP: GeoIPSectionData,
        EntityAggregateSections.Labels: LabelsSectionData,
    }

    def __init__(self, data: List[JsonObject]):
        self._sections = {}  # type: Dict[EntityAggregateSections,Any]
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
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        val = self._sections[EntityAggregateSections.AssociatedAttributes]
        return val  # type: ignore

    @property
    def natural_attributes(self) -> SectionView[List[AttributesSectionData]]:
        """Natural attributes of the entity.

        Raises:
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        val = self._sections[EntityAggregateSections.NaturalAttributes]
        return val  # type: ignore

    @property
    def threat(self) -> SectionView[ThreatSectionData]:
        """Entity threat status.

        Raises:
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.Threat]  # type: ignore

    @property
    def av_scan_statistics(self) -> SectionView[AVScanStatisticsSectionData]:
        """AV scanning statistics.

        Raises:
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        val = self._sections[EntityAggregateSections.AVScanStatistics]
        return val  # type: ignore

    @property
    def geo_ip(self) -> SectionView[GeoIPSectionData]:
        """GeoIP information.

        Raises:
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.GeoIP]  # type: ignore

    @property
    def labels(self) -> SectionView[LabelsSectionData]:
        """Labels of the entity.

        Raises:
            :class:`~cybsi.api.observable.SectionNotFoundError`:
                Section is absent in the :class:`~cybsi.api.observable.SectionsView`.
        """
        return self._sections[EntityAggregateSections.Labels]  # type: ignore
