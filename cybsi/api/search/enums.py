from enum_tools.documentation import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class QueryCompatibility(CybsiAPIEnum):
    """Stored query compatibility."""

    Replist = "Replist"  #: doc: Replists.
