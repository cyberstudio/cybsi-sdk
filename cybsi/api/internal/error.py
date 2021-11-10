from ..error import CybsiError


class CybsiInvalidViewDataError(CybsiError):
    """Received invalid response content from API.

    Not exported because it's used when API response
    doesn't follow the contract. Ideally, it shouldn't be thrown,
    but when it's thrown, this error simplifies cause analysis.
    """

    pass
