import datetime

from enum import Enum

from enum_tools.documentation import document_enum

from ..internal import JsonObjectView


@document_enum
class TokenType(Enum):
    """Token type."""

    Bearer = "Bearer"  # doc: Authentication is made using Bearer token type


class TokenView(JsonObjectView):
    """Authorization token view."""

    @property
    def access_token(self) -> str:
        """Access token. A cryptic string."""
        return self._get("accessToken")

    @property
    def type(self) -> TokenType:
        """Token type."""
        return TokenType(self._get("tokenType"))

    @property
    def expires_in(self) -> datetime.timedelta:
        """Token lifetime until expiration."""
        seconds = int(self._get("expiresIn"))
        return datetime.timedelta(seconds=seconds)
