from enum import Enum


class ShareLevels(Enum):
    White:  'ShareLevels' = 'White'
    Green:  'ShareLevels' = 'Green'
    Amber:  'ShareLevels' = 'Amber'
    Red:    'ShareLevels' = 'Red'


class EntityTypes(Enum):
    IPAddress:      'EntityTypes' = 'IPAddress'
    DomainName:     'EntityTypes' = 'DomainName'
    File:           'EntityTypes' = 'File'
    EmailAddress:   'EntityTypes' = 'EmailAddress'
    PhoneNumber:    'EntityTypes' = 'PhoneNumber'
    Identity:       'EntityTypes' = 'Identity'
    URL:            'EntityTypes' = 'URL'


class EntityKeyTypes(Enum):
    String:         'EntityKeyTypes' = 'String'
    MD5:            'EntityKeyTypes' = 'MD5Hash'
    SHA1:           'EntityKeyTypes' = 'SHA1Hash'
    SHA256:         'EntityKeyTypes' = 'SHA256Hash'
    IANAID:         'EntityKeyTypes' = 'IANAID'
    RIPEID:         'EntityKeyTypes' = 'RIPEID'
    NICHandle:      'EntityKeyTypes' = 'NICHandle'


class AttributeNames(Enum):
    Class:                  'AttributeNames' = 'Class'
    DisplayNames:           'AttributeNames' = 'DisplayNames'
    IsIoC:                  'AttributeNames' = 'IsIoC'
    IsTrusted:              'AttributeNames' = 'IsTrusted'
    MalwareFamilyAliases:   'AttributeNames' = 'MalwareFamilyAliases'
    Names:                  'AttributeNames' = 'Names'
    NodeRoles:              'AttributeNames' = 'NodeRoles'
    Sectors:                'AttributeNames' = 'Sectors'
    Size:                   'AttributeNames' = 'Size'
    IsMalicious:            'AttributeNames' = 'IsMalicious'
