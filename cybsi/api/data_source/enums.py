from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class DataSourceListOrder(CybsiAPIEnum):
    """Sorting field of data sources."""

    FullName = "FullName"
    """Sort by FullName means sort by `LongName` of type + `LongName` of datasource."""


@document_enum
class DataSourceTypeListOrder(CybsiAPIEnum):
    """Sorting field of data source types."""

    ShortName = "ShortName"  # doc: Sort by ShortName field.
    LongName = "LongName"  # doc: Sort by LongName field.
