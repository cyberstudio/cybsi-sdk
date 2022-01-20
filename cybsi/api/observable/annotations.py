from typing import Any, Dict, Optional

from ..internal import BaseAPI
from ..pagination import Cursor, Page


class AnnotationsAPI(BaseAPI):
    """Annotations API"""

    _path = "/observable/annotation"

    def filter(
        self,
        prefix: str,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page[str]:
        """Filter labels of observable entities.

        Note:
            Calls `GET /observable/annotation/labels`.
        Args:
            prefix: Label prefix.
                Prefix length must be in range [2, 50].
            cursor: Page cursor.
            limit: Page limit.
        Returns: List of labels.
            Labels are sorted in a stable best match order.
        """

        params: Dict[str, Any] = {}
        if prefix is not None:
            params["prefix"] = prefix
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{self._path}/labels"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, str)
        return page
