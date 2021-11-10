from enum import Enum

from enum_tools import document_enum


@document_enum
class ArtifactTypes(Enum):
    Archive = "Archive"  #: doc: Archive.
    FileSample = "FileSample"  #: doc: File sample.
    NetworkTraffic = "NetworkTraffic"  #: doc: Network traffic.
