from enum_tools.documentation import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class Status(CybsiAPIEnum):
    """License status."""

    Valid = "Valid"  # doc: Valid current license. Excludes all other statuses.
    Expired = "Expired"  # doc: The license has expired.
    Inactive = "Inactive"  # doc: Removed or deactivated.
