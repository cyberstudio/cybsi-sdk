from enum_tools.documentation import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class ShareLevels(CybsiAPIEnum):
    """Information share level, according to Traffic Light Protocol."""

    White = "White"
    """Disclosure is not limited."""
    Green = "Green"
    """Limited disclosure, restricted to the community."""
    Amber = "Amber"
    """Limited disclosure, restricted to participants’ organizations."""
    Red = "Red"
    """Not for disclosure, restricted to participants only."""


@document_enum
class EntityTypes(CybsiAPIEnum):
    """Entity types."""

    IPAddress = "IPAddress"  # doc: IPv4 or IPv6 address.
    DomainName = "DomainName"  # doc: Domain name.
    File = "File"  # doc: File.
    EmailAddress = "EmailAddress"  # doc: Email address.
    PhoneNumber = "PhoneNumber"  # doc: Phone number.
    Identity = "Identity"  # doc: Identity.
    URL = "URL"  # doc: URL.


@document_enum
class EntityKeyTypes(CybsiAPIEnum):
    """Natural entity key types."""

    String = "String"  # doc: String identifying entity.
    MD5 = "MD5Hash"  # doc: File MD5 hash.
    SHA1 = "SHA1Hash"  # doc: File SHA1 hash.
    SHA256 = "SHA256Hash"  # doc: File SHA256 hash.
    IANAID = "IANAID"  # doc: Identity identifier in IANA registry.
    NICHandle = "NICHandle"  # doc: Identity identifier in NIC database.


@document_enum
class AttributeNames(CybsiAPIEnum):
    """Entity attribute names.

    See Also:
        See :ref:`attributes`
        for complete information about available attributes.
    """

    Class = "Class"
    """
        Identity class. Attribute value type is enum,
        see :class:`IdentityClass`.
        Attribute belongs to `Identity` entity type.
    """
    DisplayNames = "DisplayNames"
    """
       Email address display names. Attribute value type is :class:`str`.
       Attribute belongs to `EmailAddress` entity type.
    """
    IsIoC = "IsIoC"
    """
      The entity is indicator of compromise. Attribute value type is :class:`bool`.
      Attribute belongs to `DomainName`, `IPAddress`, `URL`,
      `EmailAddress`, `PhoneNumber`, `File` entity type.
    """
    IsTrusted = "IsTrusted"
    """
      The entity is trusted. Attribute value type is :class:`bool`.
      Attribute belongs to `DomainName`, `IPAddress`, `URL`,
      `EmailAddress`, `File` entity type.
    """
    Names = "Names"
    """
      Names of the entity. Attribute value type is :class:`str`.
      Attribute belongs to `Identity`, `File` entity type.
    """
    NodeRoles = "NodeRoles"
    """
      The role of the node in a network.  Attribute value type is enum,
      see :class:`NodeRole`.
      Attribute belongs to `DomainName`, `IPAddress` entity type.
    """
    Sectors = "Sectors"
    """
      Identity industry sector. Attribute value type is enum,
      see :class:`IndustrySector`.
      Attribute belongs to `Identity` entity type.
    """
    Size = "Size"
    """
      Entity size. Attribute value type is :class:`int`.
      Attribute belongs to `File` entity type.
    """
    IsDGA = "IsDGA"
    """
      The domain was generated by algorithm. Attribute value type is :class:`bool`.
      Attribute belongs to `DomainName` entity type.
    """
    MalwareClasses = "MalwareClasses"
    """
      .. versionadded:: 2.9

      The file belongs to malware class.
      Attribute value type is
      :class:`~cybsi.api.dictionary.api.DictItemAttributeValue`.
      Attribute belongs to `File` entity type.
    """
    MalwareFamilies = "MalwareFamilies"
    """
      .. versionadded:: 2.9

      The file belongs to a malware family.
      Attribute value type is
      :class:`~cybsi.api.dictionary.api.DictItemAttributeValue`.
      Attribute belongs to `File` entity type.
    """
    RelatedMalwareFamilies = "RelatedMalwareFamilies"
    """
       .. versionadded:: 2.9

       The entity belongs to related malware family.
       Attribute value type is
       :class:`~cybsi.api.dictionary.api.DictItemAttributeValue`.
       Attribute belongs to `DomainName`, `IPAddress`, `URL`,
       `EmailAddress` entity type.
    """
    IsDelegated = "IsDelegated"
    """
      .. versionadded:: 2.9

      Domain name is delegated if DNS servers are specified.
      Attribute value type is :class:`bool`.
      Attribute belongs to `DomainName` entity type.
    """
    Statuses = "Statuses"
    """
      .. versionadded:: 2.9

      Domain name or IP address status obtained from Whois.
      Attribute value type is
      :class:`~cybsi.api.dictionary.api.DictItemAttributeValue`.
      Attribute belongs to `DomainName`, `IPAddress` entity type.
    """
    ASN = "ASN"
    """
      .. versionadded:: 2.9

      Autonomous system number.
      Attribute value type is :class:`int`.
      Attribute belongs to `IPAddress` entity type.
    """
    RegionalInternetRegistry = "RegionalInternetRegistry"
    """
      .. versionadded:: 2.9

      IP address belongs to one of the regional internet registrars.
      Attribute value type is
      :class:`~cybsi.api.observable.enums.RegionalInternetRegistry`.
      Attribute belongs to `IPAddress` entity type.
    """
    ThreatCategory = "ThreatCategory"
    """
      .. versionadded:: 2.9

      The entity threat category.
      Attribute value type is  :class:`~cybsi.api.observable.enums.ThreatCategory`.
      Attribute belongs to `File` entity type.
    """
    RelatedThreatCategory = "RelatedThreatCategory"
    """
      .. versionadded:: 2.9

      The threat category with which the entity has a relationship.
      Attribute value type is
      :class:`~cybsi.api.observable.enums.RelatedThreatCategory`.
      Attribute belongs to  `DomainName`, `IPAddress`, `URL`,
      `EmailAddress` entity types.
    """
    MalwareNames = "MalwareNames"
    """
      .. versionadded:: 2.9

      The entity malware name. Attribute value type is :class:`str`.
      Attribute belongs to `File` entity type.
    """


@document_enum
class NodeRole(CybsiAPIEnum):
    """Node roles."""

    CnC = "CnC"  # doc: CnC node.
    TorNode = "TorNode"  # doc: Tor node of any type.
    TorExitNode = "TorExitNode"  # doc: Tor exit node.
    Proxy = "Proxy"  # doc: Proxy server.
    NameServer = "NameServer"  # doc: Name server.
    MailExchanger = "MailExchanger"  # doc: Mail server.
    Phishing = "Phishing"  # doc: Phishing server.


@document_enum
class IdentityClass(CybsiAPIEnum):
    """Identity classes."""

    Individual = "Individual"
    """A single person."""
    Group = "Group"
    """An informal collection of people, without formal governance."""
    Organization = "Organization"
    """A formal organization of people, with governance."""
    Class = "Class"
    """A class of entities, such as all hospitals, all Europeans etc."""


@document_enum
class IndustrySector(CybsiAPIEnum):
    """Industry Sectors."""

    Agriculture = "Agriculture"
    Aerospace = "Aerospace"
    Automotive = "Automotive"
    Communications = "Communications"
    Construction = "Construction"
    Defence = "Defence"
    Education = "Education"
    Energy = "Energy"
    Entertainment = "Entertainment"
    FinancialServices = "FinancialServices"
    GovernmentNational = "GovernmentNational"
    GovernmentRegional = "GovernmentRegional"
    GovernmentLocal = "GovernmentLocal"
    GovernmentPublicServices = "GovernmentPublicServices"
    Healthcare = "Healthcare"
    HospitalityLeisure = "HospitalityLeisure"
    Infrastructure = "Infrastructure"
    Insurance = "Insurance"
    Manufacturing = "Manufacturing"
    Mining = "Mining"
    NonProfit = "NonProfit"
    Pharmaceuticals = "Pharmaceuticals"
    Retail = "Retail"
    Technology = "Technology"
    Telecommunications = "Telecommunications"
    Transportation = "Transportation"
    Utilities = "Utilities"
    HostingProvider = "TelecommunicationsHostingProvider"
    DomainRegistrar = "TelecommunicationsDomainRegistrar"
    MobilePhoneOperator = "TelecommunicationsMobilePhoneOperator"
    FixedLinePhoneOperator = "TelecommunicationsFixedLinePhoneOperator"


@document_enum
class RelationshipKinds(CybsiAPIEnum):
    """Kind of a relationship between entities.

    See Also:
        See :ref:`relationships`
        for complete information about available relationships.
    """

    Has = "Has"
    Contains = "Contains"
    BelongsTo = "BelongsTo"  # doc: Deprecated.
    ConnectsTo = "ConnectsTo"
    Drops = "Drops"
    Uses = "Uses"
    Owns = "Owns"
    Supports = "Supports"
    ResolvesTo = "ResolvesTo"
    VariantOf = "VariantOf"  # doc: Deprecated.
    Targets = "Targets"
    Exploits = "Exploits"
    Hosts = "Hosts"
    Serves = "Serves"
    Locates = "Locates"


@document_enum
class EntityAggregateSections(CybsiAPIEnum):
    """Entity aggregation section."""

    AssociatedAttributes = "AssociatedAttributes"
    NaturalAttributes = "NaturalAttributes"
    Threat = "Threat"
    AVScanStatistics = "AVScanStatistics"
    GeoIP = "GeoIP"
    Labels = "Labels"


@document_enum
class ThreatStatus(CybsiAPIEnum):
    """Threat status."""

    Unknown = "Unknown"
    Malicious = "Malicious"
    NonMalicious = "NonMalicious"


@document_enum
class LinkDirection(CybsiAPIEnum):
    """Direction of links."""

    Forward = "Forward"
    Reverse = "Reverse"


@document_enum
class RegionalInternetRegistry(CybsiAPIEnum):
    """Regional internet registrars."""

    RIPE = "RIPE"
    APNIC = "APNIC"
    ARIN = "ARIN"
    AFRINIC = "AFRINIC"
    LACNIC = "LACNIC"


@document_enum
class ThreatCategory(CybsiAPIEnum):
    """Threat categories."""

    Clean = "Clean"
    Riskware = "Riskware"
    Adware = "Adware"
    Malware = "Malware"


@document_enum
class RelatedThreatCategory(CybsiAPIEnum):
    """Related threat categories."""

    Riskware = "Riskware"
    Adware = "Adware"
    Malware = "Malware"
