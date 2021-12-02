import uuid
from typing import Optional

from ..common import RefView
from ..internal import (
    BaseAPI,
    JsonObjectForm,
)

from .api_types import DataSourceTypesView


class DataSourcesAPI(BaseAPI):
    """API to operate data source."""

    _path = "/data-sources"

    def view(self, datasource_uuid: uuid.UUID) -> "DataSourcesView":
        """Get the data source view.

        Note:
            Calls `GET /data-sources/{datasource_uuid}`.
        Args:
            datasource_uuid: Data source UUID.
        Returns:
            View of the data source.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
        """
        path = f"{self._path}/{datasource_uuid}"
        r = self._connector.do_get(path)
        return DataSourcesView(r.json())

    def me(self) -> "DataSourcesView":
        """Get data source assosiated with current client.

        Note:
            Calls `GET /data-sources/me`.
        """
        path = f"{self._path}/me"
        r = self._connector.do_get(path)
        return DataSourcesView(r.json())

    def register(self, form: "DataSourcesForm") -> RefView:
        """Register a data source.

        Note:
            Calls `POST /data-sources`.
        Args:
            datasource: Filled data source form.
        Raises:
            :class:`~cybsi.api.error.DuplicateDataSource`: Data source already exist.
            :class:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`:
                Data source type not found.
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())


class DataSourcesForm(JsonObjectForm):
    """Data source form.

    This is the form you need to fill to register data source.

    Args:
        type_uuid: Id of data source type.
        name: Data source identifier. Must be unique name for data source type.
        long_name: Human-readable data source name.
        manual_confidence: Manually set confidence of the data source. Overrides
            confidence of the data source type. Set between 0 and 1.
    Return:
        Data source register form.
    """

    def __init__(
        self,
        type_uuid: uuid.UUID,
        name: str,
        long_name: str,
        manual_confidence: Optional[float] = None,
    ):
        super().__init__()
        self._data["typeUUID"] = type_uuid
        self._data["name"] = name
        self._data["longName"] = long_name
        if manual_confidence is not None:
            self._data["manualConfidence"] = manual_confidence


class DataSourcesView(RefView):
    """View of data source."""

    @property
    def type(self) -> DataSourceTypesView:
        """Data source type."""
        return DataSourceTypesView(self._get("type"))

    @property
    def name(self) -> str:
        """Data source identifier. Must be unique name for data source type."""
        return self._get("name")

    @property
    def long_name(self) -> str:
        """Human-readable data source name."""
        return self._get("longName")

    @property
    def confidence(self) -> float:
        """Confidence of data source."""
        return self._get("confidence")

    @property
    def manual_confidence(self) -> Optional[float]:
        """Manually set confidence of the data source. Overrides
        confidence of the data source type."""
        return self._get_optional("manualConfidence")
