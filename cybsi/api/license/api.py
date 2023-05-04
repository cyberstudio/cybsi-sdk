from datetime import datetime
from typing import Any, List, Optional

from ..internal import BaseAPI, JsonObjectView, parse_rfc3339_timestamp
from .enums import Status


class LicensesAPI(BaseAPI):
    """API to operate licenses.

    .. versionadded:: 2.10
    """

    _path = "/license"
    _info_path = "/license/info"

    def upload(self, data: Any):
        """Upload license.

        .. versionadded:: 2.10
        Note:
            Calls `PUT /license`.
        Args:
            data: File-like object. Data must be present
                as a `license-access-token.key` file or
                as zip-archive with nested `license-access-token.key`.
                If you have key in bytes, wrap them in BytesIO.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.LicenseFileMissing`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.CorruptedLicense`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.ExpiredLicense`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UnsupportedProduct`
        """
        self._connector.do_put(path=self._path, content=data)

    def info(self) -> "LicenseInfoView":
        """Get the license information.

        .. versionadded:: 2.10
        Note:
            Calls `GET /license/info`.
        Returns:
            View of the license info.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: License not found.
        """

        resp = self._connector.do_get(path=self._info_path)
        return LicenseInfoView(resp.json())


class LicenseInfoView(JsonObjectView):
    """License information view."""

    @property
    def no(self) -> int:
        """License serial number."""
        return self._get("no")

    @property
    def expires_at(self) -> datetime:
        """License expiration time."""
        return parse_rfc3339_timestamp(self._get("expiresAt"))

    @property
    def updated_at(self) -> Optional[datetime]:
        """Time of the last license update from the update server.
        :data:`None` if license wasn't updated yet.
        """
        return self._map_optional("updatedAt", parse_rfc3339_timestamp)

    @property
    def status(self) -> List[Status]:
        """License status (flag set)."""
        return [Status(s) for s in self._get("status")]
