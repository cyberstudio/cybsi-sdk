from typing import List

from .entity import EntityView
from .enums import EntityTypes, RelationshipKinds, LinkDirection
from ..internal import JsonObjectView


class EntityLinksForecastView(JsonObjectView):
    """Entity links forecast view."""

    @property
    def link(self) -> "LinkForecastView":
        """Link forecast view."""
        return LinkForecastView(self._get("link"))

    @property
    def confidence(self) -> float:
        """Confidence of forecast."""
        return self._get("confidence")


class LinkForecastView(JsonObjectView):
    """Link forecast view."""

    @property
    def url(self) -> str:
        """URL of relationship forecast detailed information."""
        return self._get("url")

    @property
    def direction(self) -> LinkDirection:
        """Link direction."""
        return LinkDirection(self._get("direction"))

    @property
    def relationKind(self) -> RelationshipKinds:
        """Relationship kind."""
        return RelationshipKinds(self._get("relationKind"))

    @property
    def related_entity(self) -> EntityView:
        """Related entity view."""
        return EntityView(self._get("relatedEntity"))


class EntityLinkStatisticView(JsonObjectView):
    """Link statistics view."""

    @property
    def link_type(self) -> "LinkTypeView":
        """Link type view."""
        return LinkTypeView(self._get("linkType"))

    @property
    def link_statistic(self) -> "LinkStatisticView":
        """Link statistic."""
        return LinkStatisticView(self._get("links"))


class LinkTypeView(JsonObjectView):
    """Link view."""

    @property
    def url(self) -> str:
        """URL of link detailed information."""
        return self._get("url")

    @property
    def direction(self) -> LinkDirection:
        """Link direction."""
        return LinkDirection(self._get("linkDirection"))

    @property
    def relationKind(self) -> RelationshipKinds:
        """Relationship kind."""
        return RelationshipKinds(self._get("relationKind"))

    @property
    def related_entities_type(self) -> EntityTypes:
        """Related entities types."""
        return EntityTypes(self._get("relatedEntitiesType"))


class LinkStatisticView(JsonObjectView):
    """Link statistic view."""

    @property
    def total(self) -> int:
        """Total number of forecasted links of this type."""
        return self._get("total")

    @property
    def confidence_distribution(self) -> List["LinkConfidenceDistirbutionView"]:
        """Distribution of number of links by confidence."""
        return [
            LinkConfidenceDistirbutionView(x)
            for x in self._get("distributionByConfidence")
        ]


class LinkConfidenceDistirbutionView(JsonObjectView):
    """Distribution of number of links by
    confidence with step of 0.1 in descenging order."""

    @property
    def confidence_range(self) -> List[float]:
        """List of confidence ranges: (from; to]."""
        return self._get("confidenceRange")

    @property
    def count(self) -> int:
        """Count of links whose forecast falls within specified range."""
        return self._get("count")
