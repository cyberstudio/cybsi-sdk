from enum import Enum

from enum_tools.documentation import document_enum


@document_enum
class QueryCompatibility(Enum):
    """Stored query compatibility."""

    Replist = "Replist"  #: doc: Replists.
