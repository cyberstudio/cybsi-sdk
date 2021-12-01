import uuid
from typing import Optional

from ..common import RefView
from ..internal import BaseAPI, JsonObjectForm


class DataSourceTypesAPI(BaseAPI):
    """API to operate data source types."""

    _path = "/data-source-types"

    def register(self, form: "DataSourceTypesForm") -> RefView:
        """Register a datasource type.

        Note:
            Calls `POST /data-source-types`.
        Args:
            form: Filled datasource type form.
        Raises:
            :class:`~cybsi.api.error.DuplicateDataSourceType`: DataSourceType
                already exist.
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())

    def view(self, type_uuid: uuid.UUID) -> "DataSourceTypesView":
        """Get an data source type view.

        Note:
            Calls `GET /data-sources-types/{datasource_uuid}`.
        Args:
            type_uuid: Data source UUID.
        Returns:
            View of the data source type.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: data source type not found.
        """
        path = f"{self._path}/{type_uuid}"
        r = self._connector.do_get(path)
        return DataSourceTypesView(r.json())


class DataSourceTypesForm(JsonObjectForm):
    """Data source type form.

    This is the form you need to fill to register data source type.

    Args:
        short_name: Data source type identifier. Must be unique across all data
            source types.
        long_name:  Human-readable data source type name.
        manual_confidence: Manually set confidence for datasource type.
            Overrides confidence of the data source type. Set between 0 and 1.
    Return:
        Datasource Type register form.
    """

    def __init__(
        self,
        short_name: str,
        long_name: str,
        manual_confidence: Optional[float] = None,
    ):
        super().__init__()
        self._data["shortName"] = short_name
        self._data["longName"] = long_name
        if manual_confidence is not None:
            self._data["manualConfidence"] = manual_confidence


class DataSourceTypesView(RefView):
    """View of data source type."""

    @property
    def short_name(self) -> str:
        """Data source type identifier. Unique across all data source types."""
        return self._get("shortName")

    @property
    def long_name(self) -> str:
        """Human-readable data source type name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence."""
        return self._get("confidence")

    @property
    def manual_confidence(self) -> Optional[float]:
        """Manually set confidence for datasource type.
        Overrides confidence of the data source type.
        """
        return self._get_optional("manualConfidence")


class DataSourceTypeCommonView(RefView):
    """Data source type short view"""

    @property
    def long_name(self) -> str:
        """Human-readable data source type name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence of data source type."""
        return self._get("confidence")