from datetime import datetime

from cybsi.api import RefView
from cybsi.api.internal import parse_rfc3339_timestamp
from cybsi.api.observable import ShareLevels
from .enums import ObservationTypes


class ObservationCommonView(RefView):
    """Observation short view."""

    @property
    def type(self) -> "ObservationTypes":
        """Observation type."""
        return ObservationTypes(self._get("type"))


class ObservationHeaderView(ObservationCommonView):
    """Observation header view."""

    @property
    def reporter(self) -> RefView:
        """Source reporting the observation."""

        return RefView(self._get("reporter"))

    @property
    def data_source(self) -> RefView:
        """Observation data source."""

        return RefView(self._get("dataSource"))

    @property
    def share_level(self) -> ShareLevels:
        """Share level."""

        return ShareLevels(self._get("shareLevel"))

    @property
    def seen_at(self) -> datetime:
        """Date and time when observation was seen."""

        return parse_rfc3339_timestamp(self._get("seenAt"))

    @property
    def registered_at(self) -> datetime:
        """Date and time when observation was registered."""

        return parse_rfc3339_timestamp(self._get("registeredAt"))
