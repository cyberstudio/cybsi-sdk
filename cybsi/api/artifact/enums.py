from enum_tools import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class ArtifactTypes(CybsiAPIEnum):
    Archive = "Archive"  #: doc: Archive.
    FileSample = "FileSample"  #: doc: File sample.
    NetworkTraffic = "NetworkTraffic"  #: doc: Network traffic.


@document_enum
class ArtifactContentDownloadCompressionTypes(CybsiAPIEnum):
    """Artifact content download compression type.

    Don't confuse it with compression of original artifact content itself!
    Those values are used only for artifact content downloading.
    Uncompress the downloaded archive to get artifact content.
    """

    ZIP = "ZIP"  # doc: ZIP archive
