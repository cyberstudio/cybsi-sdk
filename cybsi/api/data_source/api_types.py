import uuid
from typing import Optional, Dict, Any

from ..api import Nullable, _unwrap_nullable, Tag
from ..view import _TaggedRefView
from .. import RefView
from ..internal import BaseAPI, JsonObjectForm


class DataSourceTypesAPI(BaseAPI):
    """API to operate data source types."""

    _path = "/data-source-types"

    def register(self, form: "DataSourceTypeForm") -> RefView:
        """Register a data source type.

        Note:
            Calls `POST /data-source-types`.
        Args:
            form: Filled data source type form.
        Raises:
            :class:`~cybsi.api.error.DuplicateDataSourceType`: DataSourceType
                already exist.
        """
        r = self._connector.do_post(path=self._path, json=form.json())
        return RefView(r.json())

    def view(self, type_uuid: uuid.UUID) -> "DataSourceTypeView":
        """Get the data source type view.

        Note:
            Calls `GET /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source UUID.
        Returns:
            View of the data source type.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
        """
        path = f"{self._path}/{type_uuid}"
        r = self._connector.do_get(path)
        return DataSourceTypeView(r)

    def edit(
        self,
        type_uuid: uuid.UUID,
        tag: Tag,
        long_name: Optional[str] = None,
        manual_confidence: Nullable[float] = None,
    ) -> None:
        """Edit the data source type.

        Note:
            Calls `PATCH /data-source-types/{type_uuid}`.
        Args:
            type_uuid: Data source type uuid.
            tag: :attr:`DataSourceTypeView.tag` value. Use :meth:`view` to retrieve it.
            long_name:  Human-readable data source type name.
                Non-empty if not :data:`None`.
            manual_confidence:
                Confidence for datasource type.
                Overrides default confidence of the data source type.
                Valid values are in [0, 1].
                :data:`~cybsi.api.common.Null` means
                that Cybsi can use default confidence.
                :data:`None` means that confidence is left unchanged.
        Raises:
            :class:`~cybsi.api.error.InvalidRequestError`:
                Provided arguments have invalid values.
            :class:`~cybsi.api.error.NotFoundError`: Data source type not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                Data source type changed since last request. Update tag and retry.
        """
        form: Dict[str, Any] = {}
        if long_name is not None:
            form["longName"] = long_name
        if manual_confidence is not None:
            form["manualConfidence"] = _unwrap_nullable(manual_confidence)
        path = f"{self._path}/{type_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)


class DataSourceTypeForm(JsonObjectForm):
    """Data source type form.

    This is the form you need to fill to register data source type.

    Args:
        short_name: Data source type identifier. Must be unique across all data
            source types. Non-empty.
        long_name:  Human-readable data source type name. Non-empty.
        manual_confidence: Confidence for datasource type.
            Overrides default confidence of the data source type.
            Valid values are in [0, 1].
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


class DataSourceTypeView(_TaggedRefView):
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
