import uuid
from typing import Optional, Dict, Any

from ..api import Nullable, _unwrap_nullable, Tag
from ..view import _TaggedRefView
from .. import RefView
from ..internal import (
    BaseAPI,
    JsonObjectForm,
)
from .api_types import DataSourceTypeCommonView


class DataSourcesAPI(BaseAPI):
    """API to operate data source."""

    _path = "/data-sources"

    def view(self, datasource_uuid: uuid.UUID) -> "DataSourceView":
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
        return DataSourceView(r)

    def me(self) -> "DataSourceView":
        """Get data source assosiated with current client.

        Note:
            Calls `GET /data-sources/me`.
        """
        path = f"{self._path}/me"
        r = self._connector.do_get(path)
        return DataSourceView(r)

    def register(self, form: "DataSourceForm") -> RefView:
        """Register a data source.

        Note:
            Calls `POST /data-sources`.
        Args:
            form: Filled data source form.
        Raises:
            :class:`~cybsi.api.error.DuplicateDataSource`: Data source already exist.
            :class:`~cybsi.api.error.SemanticErrorCodes.DataSourceTypeNotFound`:
                Data source type not found.
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())

    def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source.

        Note:
            Calls `PATCH /data-sources/{source_uuid}`.
        Args:
            type_uuid: Data source uuid.
            tag: :attr:`DataSourceView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source name. Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for data source.
                Overrides confidence of the data source inherited from data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.common.Null` means
                that Cybsi can use confidence provided by data source type.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source changed since last request. Update tag and retry.
        """
        form: Dict[str, Any] = {}
        if long_name is not None:
            form["longName"] = long_name
        if manual_confidence is not None:
            form["manualConfidence"] = _unwrap_nullable(manual_confidence)
        path = f"{self._path}/{type_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)


class DataSourceForm(JsonObjectForm):
    """Data source form.

    This is the form you need to fill to register data source.

    Args:
        type_uuid: Id of data source type.
        name: Data source identifier. Must be unique name for data source type.
        long_name: Human-readable data source name.
        manual_confidence:
            Confidence of the data source.
            Overrides confidence of the data source inherited from data source type.
            Valid values are in [0, 1].
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


class DataSourceView(_TaggedRefView):
    """View of data source."""

    @property
    def type(self) -> DataSourceTypeCommonView:
        """Data source type."""
        return DataSourceTypeCommonView(self._get("type"))

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


class DataSourceCommonView(RefView):
    """Data source short view."""

    @property
    def long_name(self) -> str:
        """Human-readable data source name."""
        return self._get("longName")

    @property
    def unique_name(self) -> str:
        """The unique identifier contains of the type `ShortName` and
        the source `Name` (ShortName/Name)."""
        return self._get("uniqueName")

    @property
    def confidence(self) -> float:
        """Confidence of data source."""
        return self._get("confidence")

    @property
    def type(self) -> "DataSourceTypeCommonView":
        """Data source type short view."""
        return DataSourceTypeCommonView(self._get("type"))
