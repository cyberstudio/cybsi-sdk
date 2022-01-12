import uuid
from typing import List, Optional

from ..internal import BaseAPI, JsonObjectForm, JsonObjectView
from ..observable import ShareLevels
from ..view import RefView, _TaggedRefView


class UsersAPI(BaseAPI):
    """Users API."""

    _path = "/users"

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
            Calls `Get /users/{user_uuid}`.
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
        >>>     roles=["EntityReader"],
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
        roles: List[str],
        password: Optional[str] = None,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        data_source_uuid: Optional[uuid.UUID] = None,
    ):
        super().__init__()
        self._data["login"] = login
        self._data["accessLevel"] = access_level.value
        self._data["roles"] = roles
        if password is not None:
            self._data["password"] = password
        if full_name is not None:
            self._data["fullName"] = full_name
        if email is not None:
            self._data["email"] = email
        if data_source_uuid is not None:
            self._data["dataSourceUUID"] = str(data_source_uuid)


class UserView(_TaggedRefView):
    """User full view."""

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
    def name(self) -> str:
        """Role name."""
        return self._get("name")
