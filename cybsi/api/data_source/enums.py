from enum import Enum

from enum_tools import document_enum


@document_enum
class DataSourceListOrder(Enum):
    """Sorting field of data sources."""

    UUID = "UUID"  #: doc: Sort by UUID field.
    FullName = "FullName"  # noqa: E501 doc: Sort by FullName means sort by `LongName` of type + `LongName` of datasource.


@document_enum
class DataSourceTypeListOrder(Enum):
    """Sorting field of data source types."""

    ShortName = "ShortName"  #: doc: Sort by ShortName field.
    LongName = "LongName"  #: doc: Sort by LongName field.
