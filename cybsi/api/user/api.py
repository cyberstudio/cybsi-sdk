import uuid
from typing import Iterable, List, Optional

from ..api import Nullable, _unwrap_nullable
from ..internal import BaseAPI, JsonObject, JsonObjectForm, JsonObjectView
from ..observable import ShareLevels
from ..pagination import Cursor, Page
from ..view import RefView, Tag, _TaggedRefView
from .enums import RoleName


class UsersAPI(BaseAPI):
    """Users API."""

    _path = "/users"
    _me_path = "/users/me"

    def register(self, form: "UserForm") -> RefView:
        """Register user.

        Note:
            Calls `POST /users`.
        Args:
            form: Filled user form.
        Returns:
            Reference to the registered user.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.ConflictError`:
                User with the specified login already exists.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        """

        resp = self._connector.do_post(path=self._path, json=form.json())
        return RefView(resp.json())

    def view(self, user_uuid: uuid.UUID) -> "UserView":
        """Get the user view.

        Note:
            Calls `GET /users/{user_uuid}`.
        Args:
            user_uuid: User UUID.
        Returns:
            Full view of the user with ETag string value.
        Raises:
            :class:`~cybsi.api.error.NotFoundError`: User not found.
        """

        path = f"{self._path}/{user_uuid}"
        resp = self._connector.do_get(path)
        return UserView(resp)

    def me(self) -> "CurrentUserView":
        """Get user associated with current client.

        Note:
            Calls `GET /users/me`.
        Returns:
            View of current user.
        """

        r = self._connector.do_get(self._me_path)
        return CurrentUserView(r.json())

    def filter(
        self,
        user_uuids: Optional[Iterable[uuid.UUID]] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
        cursor: Optional[Cursor] = None,
        limit: Optional[int] = None,
    ) -> Page["UserCommonView"]:
        """Filter users.

        Note:
            Calls `GET /users`.
        Args:
            user_uuids: User identifiers.
                Filter users by specified user UUIDs.
            data_source_uuid: Data source identifier.
                Filter users by associated data source UUID.
            cursor: Page cursor.
            limit: Page limit.
        Return:
            Page with user common views and next page cursor.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: query arguments contain errors.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
        Usage:
            >>> import uuid
            >>> from cybsi.api import CybsiClient
            >>> from cybsi.api.pagination import chain_pages
            >>>
            >>> client: CybsiClient
            >>> # filter users by specified data source uuid
            >>> started_page = client.users.filter(
            >>>     data_source_uuid=uuid.UUID("007c3927-1ef6-474a-b89b-d6feb3c73871"),
            >>> )
            >>> for item in chain_pages(started_page):
            >>>     # do something with users
            >>>     print(item)
            >>> pass
        """

        params: JsonObject = {}
        if data_source_uuid is not None:
            params["dataSourceUUID"] = str(data_source_uuid)
        if user_uuids is not None:
            params["uuid"] = [str(u) for u in user_uuids]
        if cursor is not None:
            params["cursor"] = str(cursor)
        if limit is not None:
            params["limit"] = str(limit)

        resp = self._connector.do_get(path=self._path, params=params)
        page = Page(self._connector.do_get, resp, UserCommonView)
        return page

    def edit(
        self,
        user_uuid: uuid.UUID,
        tag: Tag,
        full_name: Nullable[str] = None,
        email: Nullable[str] = None,
        data_source_uuid: Nullable[uuid.UUID] = None,
        access_level: Optional[ShareLevels] = None,
        roles: Optional[Iterable[RoleName]] = None,
        password: Optional[str] = None,
        is_disabled: Optional[bool] = None,
    ):
        """Edit user.

        Note:
            Calls `PATCH /users/{user_uuid}`.
        Args:
            user_uuid: User identifier.
            tag: :attr:`UserView.tag` value. Use :meth:`view` to retrieve it.
            full_name: User full name.
                Name must be less than or equal to 250 characters.
            email: User email. Email length must be in range [3, 254].
            data_source_uuid: Associated data source UUID.
                Cannot be changed for users of external providers.
            access_level: User access level.
            roles: List of user role names.
            password: User password. Password length must be in range [4, 50].
                Cannot be changed for users of external providers.
            is_disabled: Disabled user flag.
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.ConflictError`:
                User with specified associated data source already exists.
            :class:`~cybsi.api.error.NotFoundError`: User not found.
            :class:`~cybsi.api.error.ResourceModifiedError`:
                User changed since last request. Retry using updated tag.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.DataSourceNotFound`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.NonLocalUser`
        """
        form: JsonObject = {}
        if full_name is not None:
            form["fullName"] = _unwrap_nullable(full_name)
        if email is not None:
            form["email"] = _unwrap_nullable(email)
        if data_source_uuid is not None:
            form["dataSourceUUID"] = str(_unwrap_nullable(data_source_uuid))
        if access_level is not None:
            form["accessLevel"] = access_level.value
        if roles is not None:
            form["roles"] = [role.value for role in roles]
        if password is not None:
            form["password"] = password
        if is_disabled is not None:
            form["isDisabled"] = is_disabled

        path = f"{self._path}/{user_uuid}"
        self._connector.do_patch(path=path, tag=tag, json=form)

    def change_my_password(self, old_password: str, new_password: str):
        """Change password of current client.

        Note:
            The password can be changed only if the password was set initially.
            Password login is not available for users without a password.

            To confirm authorization and exclude situations when
            the password is changed using the API key,
            you must specify the valid current user password in the request.
        Note:
            Calls `PUT /users/me/password`.
        Args:
            old_password: Old user password. Password length must be in range [4, 50].
            new_password: New user password. Password length must be in range [4, 50].
        Raises:
            :class:`~cybsi.api.error.SemanticError`: Form contains logic errors.
            :class:`~cybsi.api.error.ForbiddenError`:
                Specified user password does not match the current one.
        Note:
            Semantic error codes specific for this method:
              * :attr:`~cybsi.api.error.SemanticErrorCodes.NonLocalUser`
              * :attr:`~cybsi.api.error.SemanticErrorCodes.PasswordAuthDisabled`
        """

        form: JsonObject = {"oldPassword": old_password, "newPassword": new_password}
        path = f"{self._me_path}/password"
        self._connector.do_put(path=path, json=form)


class UserForm(JsonObjectForm):
    """User form.

    This is the form you need to fill to register user.

    Args:
        login: User login. Login should consist of characters
            without spaces (`[a-zA-Z0-9_-]`) and have length in the range [1, 250].
        access_level: User access level.
        roles: List of user role names.
        password: User password. Password length must be in range [4, 50].
            if ``password`` is :data:`None` then
            the user will not be able to enter the system by password.
        full_name: User full name. Name must be less than or equal to 250 characters.
        email: User email. Email length must be in range [3, 254].
        data_source_uuid: Associated data source UUID.
            If ``data_source_uuid`` is :data:`None` then data source will be created and
            assigned when the user first tries to register TI data.

    Usage:
        >>> from cybsi.api.observable import ShareLevels
        >>> from cybsi.api.user import UserForm
        >>>
        >>> userForm = UserForm(
        >>>     login="user_test",
        >>>     access_level=ShareLevels.Green,
        >>>     roles=[RoleName.EntityReader],
        >>>     password="string",
        >>>     full_name="Test Tester",
        >>>     email="test@pt.com",
        >>> )
        >>> pass
    """

    def __init__(
        self,
        login: str,
        access_level: ShareLevels,
        roles: Iterable[RoleName],
        password: Optional[str] = None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
    ):
        super().__init__()
        self._data["login"] = login
        self._data["accessLevel"] = access_level.value
        self._data["roles"] = [role.value for role in roles]
        if password is not None:
            self._data["password"] = password
        if full_name is not None:
            self._data["fullName"] = full_name
        if email is not None:
            self._data["email"] = email
        if data_source_uuid is not None:
            self._data["dataSourceUUID"] = str(data_source_uuid)


class UserCommonView(RefView):
    """User common view."""

    @property
    def login(self) -> str:
        """User login."""
        return self._get("login")

    @property
    def full_name(self) -> Optional[str]:
        """User full name."""
        return self._get_optional("fullName")

    @property
    def email(self) -> Optional[str]:
        """User email."""
        return self._get_optional("email")

    @property
    def is_disabled(self) -> bool:
        """Disabled user flag."""
        return self._get("isDisabled")

    @property
    def auth_provider_id(self) -> str:
        """Authentication provider ID."""
        return self._get("authProviderID")


class UserView(_TaggedRefView, UserCommonView):
    """User full view."""

    @property
    def access_level(self) -> ShareLevels:
        """User access level."""
        return ShareLevels(self._get("accessLevel"))

    @property
    def roles(self) -> List["RoleCommonView"]:
        """List of user role."""
        return [RoleCommonView(r) for r in self._get("roles")]

    @property
    def permissions(self) -> List[str]:
        """List of permissions derived from user roles."""
        return self._get("permissions")

    @property
    def data_source(self) -> Optional[RefView]:
        """Associated data source."""
        return self._map_optional("dataSource", RefView)


class RoleCommonView(JsonObjectView):
    """Role common view."""

    @property
    def uuid(self) -> uuid.UUID:
        """Role UUID."""
        return uuid.UUID(self._get("uuid"))

    @property
    def name(self) -> RoleName:
        """Role name."""
        return RoleName(self._get("name"))


class CurrentUserView(UserCommonView):
    """Current user view."""

    @property
    def access_level(self) -> ShareLevels:
        """User access level."""
        return ShareLevels(self._get("accessLevel"))

    @property
    def permissions(self) -> List[str]:
        """List of permissions derived from user roles."""
        return self._get("permissions")

    @property
    def data_source(self) -> Optional[RefView]:
        """Associated data source."""
        return self._map_optional("dataSource", RefView)
