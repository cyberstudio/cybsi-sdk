import asyncio
import json
import logging
import threading
import uuid
from datetime import datetime
from typing import AsyncGenerator, Generator, Iterable, List, Optional, Tuple
from urllib.parse import urljoin

import httpx

from ..error import _raise_cybsi_error
from ..internal import (
    BaseAPI,
    JsonObject,
    JsonObjectForm,
    JsonObjectView,
    parse_rfc3339_timestamp,
    rfc3339_timestamp,
)
from ..pagination import Cursor, Page
from ..user import ActionSet, ResourceName
from ..view import Tag, _TaggedRefView
from .token import TokenView

logger = logging.getLogger(__name__)


class APIKeyAuth(httpx.Auth):
    """Authomatically handles authentication
    of :class:`~cybsi.api.CybsiClient` or :class:`~cybsi.api.CybsiAsyncClient`
    requests using API key.

    Args:
        api_url: Cybsi auth API URL. Usually equal to CybsiClient config API URL.
        api_key: Cybsi API key.
        ssl_verify: enable SSL verification. Deprecated, has no effect.
            Uses value set for CybsiClient config.
    Usage:
        >>> from cybsi.api import APIKeyAuth, Config, CybsiClient
        >>> api_url = "http://localhost:80/api"
        >>> api_key = "8Nqjk6V4Q_et_Rf5EPu4SeWy4nKbVPKPzKJESYdRd7E"
        >>> auth = APIKeyAuth("", api_key)
        >>> config = Config(api_url, auth)  # Consider using :attr:`Config.api_key`
        >>> client = CybsiClient(config)
        >>> client.observations
        <cybsi_sdk.client.observation.ObservationsAPI object at 0x7f57a293c190>
    """

    requires_response_body = True  # instructs httpx to pass token request response body

    _get_token_path = "auth/token"

    def __init__(self, *, api_url: str, api_key: str, ssl_verify: bool = True):
        # See https://www.python-httpx.org/advanced/#customizing-authentication
        self._api_key = api_key
        self._api_url = api_url
        self._sync_lock = threading.RLock()
        self._async_lock = asyncio.Lock()
        self._token = ""

    def sync_auth_flow(
        self, request: httpx.Request
    ) -> Generator[httpx.Request, httpx.Response, None]:
        token = self._token
        if token:
            request.headers["Authorization"] = self._token
            response = yield request
            if response.status_code != 401:
                return

        with self._sync_lock:
            if self._token == token:
                token_response = yield self._build_token_request(request)
                self._update_token(token_response, token_response.read())
            request.headers["Authorization"] = self._token
            yield request

    async def async_auth_flow(
        self, request: httpx.Request
    ) -> AsyncGenerator[httpx.Request, httpx.Response]:
        token = self._token
        if token:
            request.headers["Authorization"] = self._token
            response = yield request
            if response.status_code != 401:
                return

        async with self._async_lock:
            if self._token == token:
                token_response = yield self._build_token_request(request)
                self._update_token(token_response, await token_response.aread())
            request.headers["Authorization"] = self._token
            yield request

    def _build_token_request(self, req) -> httpx.Request:
        token_url = urljoin(self._api_url, self._get_token_path)
        headers = {
            "Accept": req.headers["Accept"],
            "User-Agent": req.headers["User-Agent"],
        }
        return httpx.Request(
            "GET",
            url=token_url,
            params={"apiKey": self._api_key},
            headers=headers,
        )

    def _update_token(
        self, token_response: httpx.Response, token_response_content: bytes
    ) -> None:
        if not token_response.is_success:
            _raise_cybsi_error(token_response)
        token = TokenView(json.loads(token_response_content))

        self._token = f"{token.type.value} {token.access_token}"


class APIKeysAPI(BaseAPI):
    """API-Keys API."""

    _path = "/api-keys"
    _users_path = "/users"
    _me_path = f"{_users_path}/me"

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

    def _filter(
        self, path: str, cursor: Optional[Cursor] = None, limit: Optional[int] = None
    ) -> Page["APIKeyCommonView"]:
        params: JsonObject = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)
        resp = self._connector.do_get(path=path, params=params)
        page = Page(self._connector.do_get, resp, APIKeyCommonView)
        return page

    def filter(
        self,
        *,
        user_uuid: uuid.UUID,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["APIKeyCommonView"]:
        """Get API keys created for user.
        Keys are ordered by creation timestamp, new first.

        Note:
            Calls `GET /users/{user_uuid}/api-keys`.
        Args:
            user_uuid: User identifier.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with user API-Key common views and next page cursor.
        """
        path = f"{self._users_path}/{user_uuid}/api-keys"
        return self._filter(path, cursor, limit)

    def filter_my(
        self,
        *,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["APIKeyCommonView"]:
        """Get API keys which API-Client owns.

        Note:
            Calls `GET /users/me/api-keys`.
            Doesn't require any permissions.
        Args:
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with user API-Key common views and next page cursor.
        .. versionadded:: 2.8
        """
        path = f"{self._me_path}/api-keys"
        return self._filter(path, cursor, limit)

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

    def view_my(self, api_key_uuid) -> "APIKeyView":
        """Get the API-Key view which API-Client owns.

        Note:
            Calls `GET /users/me/api-keys/{api_key_id}`.
            Doesn't require any permissions.
        Args:
            api_key_uuid: API-Key identifier.
        Returns:
            Full view of the API-Key include ETag value.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: User API-Key not found.
            :class:`~cybsi.api.error.SemanticError`: Semantic error.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.NotOwner`.
        .. versionadded:: 2.8
        """

        path = f"{self._me_path}/api-keys/{api_key_uuid}"
        resp = self._connector.do_get(path)
        return APIKeyView(resp)

    @staticmethod
    def _build_edit_api_key_form(
        description: Optional[str] = None, revoked: Optional[bool] = None
    ) -> JsonObject:
        form: JsonObject = {}
        if description is not None:
            form["description"] = description
        if revoked is not None:
            form["revoked"] = revoked
        return form

    def edit(
        self,
        api_key_id: uuid.UUID,
        tag: Tag,
        *,
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
            :class:`~cybsi.api.error.ResourceModifiedError`:
                API-Key changed since last request. Retry using updated tag.
            :class:`~cybsi.api.error.NotFoundError`: User API-Key not found.
        """

        path = f"{self._path}/{api_key_id}"
        form = self._build_edit_api_key_form(description, revoked)
        self._connector.do_patch(path=path, tag=tag, json=form)

    def edit_my(
        self,
        api_key_id: uuid.UUID,
        tag: Tag,
        *,
        description: Optional[str] = None,
        revoked: Optional[bool] = None,
    ):
        """Edit API-Key which API-Client owns.

        Warning:
            Key revocation is an irreversible operation.
        Note:
            Calls `PATCH /users/me/api-keys/{api_key_id}`.
            Doesn't require any permissions.
        Args:
            api_key_id: API-Key identifier.
            tag: :attr:`APIKeyView.tag` value. Use :meth:`view` to retrieve it.
            description: API-Key description.
            revoked: API-Key revoked flag. Key revocation is an irreversible operation.
        Raises:
            :class:`~cybsi.api.error.ResourceModifiedError`:
                API-Key changed since last request. Retry using updated tag.
            :class:`~cybsi.api.error.NotFoundError`: User API-Key not found.
            :class:`~cybsi.api.error.SemanticError`: Semantic error.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.NotOwner`.
        .. versionadded:: 2.8
        """

        path = f"{self._me_path}/api-keys/{api_key_id}"
        form = self._build_edit_api_key_form(description, revoked)
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
        *,
        description: Optional[str] = None,
        permissions: Iterable[Tuple[ResourceName, ActionSet]] = [],
    ):
        super().__init__()
        self._data["expiresAt"] = rfc3339_timestamp(expires_at)
        if description is not None:
            self._data["description"] = description
        if permissions:
            self._data["permissions"] = [
                ":".join([res.value, act]) for res, act in permissions
            ]


class APIKeyRefView(JsonObjectView):
    """API-Key reference view."""

    @property
    def uuid(self) -> uuid.UUID:
        """API-Key identifier."""
        return uuid.UUID(self._get("id"))

    @property
    def url(self) -> Optional[str]:
        """URL to get full API-Key view.
        Property is presented if :class:`~cybsi.api.client.Config`
        embed_object_url is True.
        """
        return self._get_optional("url")

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
    def url(self) -> Optional[str]:
        """URL to get API-Key full view.
        Property is presented if :class:`~cybsi.api.client.Config`
        embed_object_url is True.
        """
        return self._get_optional("url")

    @property
    def description(self) -> Optional[str]:
        """API-Key description."""
        return self._get_optional("description")

    @property
    def created_at(self) -> datetime:
        """Creation date."""
        return parse_rfc3339_timestamp(self._get("createdAt"))

    @property
    def expires_at(self) -> Optional[datetime]:
        """Expiration date. :data:`None` if it shouldn't expire.

        The API-Key is automatically revoked after the expiration date."""
        return self._map_optional("expiresAt", parse_rfc3339_timestamp)

    @property
    def last_used_at(self) -> Optional[datetime]:
        """Last used date. :data:`None` if it wasn't used yet."""
        return self._map_optional("lastUsedAt", parse_rfc3339_timestamp)

    @property
    def revoked(self) -> bool:
        """API-Key revoked flag."""
        return self._get("revoked")

    @property
    def permissions(self) -> List[Tuple[ResourceName, ActionSet]]:
        """List of permissions."""

        permissions: List[Tuple[ResourceName, ActionSet]] = []

        for raw_perm in self._get("permissions"):
            res, act = raw_perm.split(":", 1)
            permissions.append((ResourceName(res), act))
        return permissions


class APIKeyView(_TaggedRefView, APIKeyCommonView):
    """API-Key full view."""

    @property
    def uuid(self) -> uuid.UUID:
        """API-Key identifier."""
        return uuid.UUID(self._get("id"))
