from enum import Enum

from enum_tools import document_enum


@document_enum
class EntitySetOperations(Enum):
    """Type of operation applied to an entity in reputation list."""

    Add = "Add"  # doc: An entity was added.
    Remove = "Remove"  # doc: An entity was removed.


@document_enum
class ReplistStatus(Enum):
    """Current status of reputation list."""

    Initializing = "Initializing"  # doc: Replist is in building process.
    Active = "Active"  # doc: Replist is enabled.
    Inactive = "Inactive"  # doc: Replist is disabled.
