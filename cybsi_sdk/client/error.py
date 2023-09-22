from .base import ResponseView


class ErrorView(ResponseView):

    @property
    def code(self) -> str:
        """Get internal error code
        """

        return self._data.get('code')

    @property
    def message(self):
        """Get error message

        :rtype: str
        """

        return self._data.get('message')
