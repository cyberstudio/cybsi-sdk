import logging
import uuid
from datetime import datetime
from typing import List, Optional

import requests

from ..error import CybsiError
from ..internal import (
    BaseAPI,
    HTTPConnector,
    JsonObject,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
    rfc3339_timestamp,
)
from ..pagination import Cursor, Page
from ..view import Tag, _TaggedRefView
from .token import TokenView

logger = logging.getLogger(__name__)


class APIKeyAuth:
    """Callable. Authomatically handles authentication
    of :class:`~cybsi.api.CybsiClient` requests using API key.

    Args:
        api_url: Cybsi API URL.
        api_key: Cybsi API key.
        ssl_verify: enable SSL verification.
    Usage:
        >>> from cybsi.api import APIKeyAuth, Config, CybsiClient
        >>> api_url = "http://localhost:80/api"
        >>> api_key = "8Nqjk6V4Q_et_Rf5EPu4SeWy4nKbVPKPzKJESYdRd7E"
        >>> auth = APIKeyAuth(api_url, api_key)
        >>> config = Config(api_url, auth)
        >>> client = CybsiClient(config)
        >>> client.observations
        <cybsi_sdk.client.observation.ObservationsAPI object at 0x7f57a293c190>
    """

    _get_token_path = "auth/token"

    def __init__(self, api_url: str, api_key: str, ssl_verify: bool = True):
        self._api_key = api_key
        self._connector = HTTPConnector(api_url, ssl_verify=ssl_verify)
        self._token = None  # type: Optional[str]

    def __call__(self, r: requests.Request):
        # Get access token from Cybsi using API key and retry HTTP
        # request if 401 response is received.
        if self._token:
            r.headers["Authorization"] = self._token

        r.register_hook("response", self._handle_401)
        return r

    def _handle_401(self, r, **kwargs):
        """Handler for 401 http response"""

        if r.status_code != 401:
            return r

        r.close()
        req = r.request.copy()

        logger.debug("request: %s %s, unauthorized.", req.method, req.url)

        resp = self._connector.do_get(
            self._get_token_path, params={"apiKey": self._api_key}
        )
        token = TokenView(resp.json())

        self._token = f"{token.type.value} {token.access_token}"
        req.headers["Authorization"] = self._token

        try:
            _r = r.connection.send(req, **kwargs)
        except Exception as exp:
            raise CybsiError("unable to send authenticated request", exp) from None

        _r.history.append(r)
        _r.request = req
        return _r


class APIKeysAPI(BaseAPI):
    """API-Keys API."""

    _path = "/api-keys"
    _users_path = "/users"

    def generate(self, user_uuid: uuid.UUID, form: "APIKeyForm") -> "APIKeyRefView":
        """Generate API-Key for user.

        Warning:
            Make sure to copy API key value because it is not stored on the server.
            Revoke API key if you suspect a leak.
        Note:
            Calls `POST /users/{userID}/api-keys`.
        Args:
            user_uuid: User identifier.
            form: APIKeyForm instance.
        Returns:
            Reference to the generated API-Key.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.PermissionsExceeded`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.UserDisabled`
        """
        path = f"{self._users_path}/{user_uuid}/api-keys"
        resp = self._connector.do_post(path=path, json=form.json())
        return APIKeyRefView(resp.json())

    def filter(
        self,
        user_uuid: uuid.UUID,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["APIKeyCommonView"]:
        """Get API keys created for user.

        Note:
            Calls `GET /users/{user_uuid}/api-keys`.
        Args:
            user_uuid: User identifier.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with user API-Key common views and next page cursor.
        """
        params: JsonObject = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        path = f"{self._users_path}/{user_uuid}/api-keys"
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, APIKeyCommonView)
        return page

    def view(self, api_key_id: uuid.UUID) -> "APIKeyView":
        """Get the API-Key view.

        Note:
            Calls `GET /api-keys/{api_key_id}`.
        Args:
            api_key_id: API-Key identifier.
        Returns:
            Full view of the API-Key include ETag value.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: User API-Key not found.
        """

        path = f"{self._path}/{api_key_id}"
        resp = self._connector.do_get(path)
        return APIKeyView(resp)

    def edit(
        self,
        api_key_id: uuid.UUID,
        tag: Tag,
        description: Optional[str] = None,
        revoked: Optional[bool] = None,
    ):
        """Edit description and/or revoke API-Key.

        Warning:
            Key revocation is an irreversible operation.
        Note:
            Calls `PATCH /api-keys/{api_key_id}`.
        Args:
            api_key_id: API-Key identifier.
            tag: :attr:`APIKeyView.tag` value. Use :meth:`view` to retrieve it.
            description: API-Key description.
            revoked: API-Key revoked flag. Key revocation is an irreversible operation.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: User API-Key not found.
        """

        form: JsonObject = {}
        if description is not None:
            form["description"] = description
        if revoked is not None:
            form["revoked"] = revoked

        path = f"{self._path}/{api_key_id}"
        self._connector.do_patch(path=path, tag=tag, json=form)


class APIKeyForm(JsonObjectForm):
    """API-Key form.

    This is the form you need to fill to generate API-Key.

    Args:
        description: API-Key description.
        expires_at: Expiration date.
            The API-Key is automatically revoked after the expiration date.
        permissions: List of permissions. If not set then
            the API-Key inherits permissions from the owner user.
    """

    def __init__(
        self,
        expires_at: datetime,
        description: Optional[str] = None,
        permissions: Optional[List[str]] = None,
    ):
        super().__init__()
        self._data["expiresAt"] = rfc3339_timestamp(expires_at)
        if description is not None:
            self._data["description"] = description
        if permissions is not None:
            self._data["permissions"] = permissions


class APIKeyRefView(JsonObjectView):
    """API-Key reference view."""

    @property
    def uuid(self) -> uuid.UUID:
        """API-Key identifier."""
        return uuid.UUID(self._get("id"))

    @property
    def url(self) -> str:
        """URL to get full API-Key view."""
        return self._get("url")

    @property
    def key(self) -> str:
        """API-Key."""
        return self._get("key")


class APIKeyCommonView(JsonObjectView):
    """API-Key common view."""

    @property
    def uuid(self) -> uuid.UUID:
        """API-Key identifier."""
        return uuid.UUID(self._get("id"))

    @property
    def url(self) -> str:
        """URL to get API-Key full view."""
        return self._get("url")

    @property
    def description(self) -> Optional[str]:
        """API-Key description."""
        return self._get_optional("description")

    @property
    def created_at(self) -> datetime:
        """Creation date."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def expires_at(self) -> datetime:
        """Expiration date.
        The API-Key is automatically revoked after the expiration date."""
        return parse_rfc3339_timestamp(self._get("expiresAt"))

    @property
    def last_used_at(self) -> datetime:
        """Last used date."""
        return parse_rfc3339_timestamp(self._get("lastUsedAt"))

    @property
    def revoked(self) -> bool:
        """API-Key revoked flag."""
        return self._get("revoked")

    @property
    def permissions(self) -> List[str]:
        """List of permissions."""
        return self._get("permissions")


class APIKeyView(_TaggedRefView, APIKeyCommonView):
    """API-Key full view."""

    @property
    def uuid(self) -> uuid.UUID:
        """API-Key identifier."""
        return uuid.UUID(self._get("id"))
