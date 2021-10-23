from .base import JsonObjectView


class ErrorView(JsonObjectView):
    """Error returned by Cybsi API"""
    @property
    def code(self) -> str:
        """Get internal error code
        """

        return self._get('code')

    @property
    def message(self):
        """Get error message

        :rtype: str
        """

        return self._get('message')