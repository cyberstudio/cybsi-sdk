from cybsi_sdk.client import base


class TokenView(base.JsonObjectView):

    @property
    def access_token(self):
        """Get access token
        """
        return self._get("accessToken")

    @property
    def type(self):
        """Get token's type
        """
        return self._get("tokenType")

    @property
    def expires_in(self):
        """Get token's expires in
        """
        return self._get("expiresIn")
