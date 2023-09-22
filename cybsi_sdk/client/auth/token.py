from cybsi_sdk.client import base


class TokenView(base.ResponseView):

    @property
    def access_token(self):
        """Get access token
        """
        return self._data.get("accessToken")

    @property
    def type(self):
        """Get token's type
        """
        return self._data.get("tokenType")

    @property
    def expires_in(self):
        """Get token's expires in
        """
        return self._data.get("expiresIn")
