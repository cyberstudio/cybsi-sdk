from os import environ

from cybsi.api import APIKeyAuth, Config, CybsiClient, Limits, Timeouts

if __name__ == "__main__":
    api_key = environ["CYBSI_API_KEY"]
    api_url = environ["CYBSI_API_URL"]

    auth = APIKeyAuth(api_url=api_url, api_key=api_key)

    # Set custom timeouts and limits of HTTP client
    limits = Limits(max_connections=100, max_keepalive_connections=20)
    timeouts = Timeouts(default=3.0)

    config = Config(api_url, auth, ssl_verify=False, timeouts=timeouts, limits=limits)
    client = CybsiClient(config)
    client.artifacts.filter()
