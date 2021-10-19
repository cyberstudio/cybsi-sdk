from enum import Enum


class ShareLevels(Enum):
    White = 'White'
    Green = 'Green'
    Amber = 'Amber'
    Red = 'Red'


class EntityTypes(Enum):
    IPAddress = 'IPAddress'
    DomainName = 'DomainName'
    File = 'File'
    EmailAddress = 'EmailAddress'
    PhoneNumber = 'PhoneNumber'
    Identity = 'Identity'
    URL = 'URL'


class EntityKeyTypes(Enum):
    String = 'String'
    MD5 = 'MD5Hash'
    SHA1 = 'SHA1Hash'
    SHA256 = 'SHA256Hash'
    IANAID = 'IANAID'
    RIPEID = 'RIPEID'
    NICHandle = 'NICHandle'


class AttributeNames(Enum):
    Class = 'Class'
    DisplayNames = 'DisplayNames'
    IsIoC = 'IsIoC'
    IsTrusted = 'IsTrusted'
    MalwareFamilyAliases = 'MalwareFamilyAliases'
    Names = 'Names'
    NodeRoles = 'NodeRoles'
    Sectors = 'Sectors'
    Size = 'Size'
    IsMalicious = 'IsMalicious'
    IsDGA = 'IsDGA'


class RelationshipKinds(Enum):
    Has = 'Has'
    Contains = 'Contains'
    BelongsToDeprecated = 'BelongsTo'
    ConnectsTo = 'ConnectsTo'
    Drops = 'Drops'
    Uses = 'Uses'
    Owns = 'Owns'
    Supports = 'Supports'
    Resolves = 'ResolvesTo'
    VariantOfDeprecated = 'VariantOf'
    Targets = 'Targets'
    Exploits = 'Exploits'
    Hosts = 'Hosts'
    Serves = 'Serves'
    Locates = 'Locates'


class ReplistOperations(Enum):
    Add = 'Add'
    Remove = 'Remove'
