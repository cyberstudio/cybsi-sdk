from enum_tools.documentation import document_enum

from cybsi.api.enum import CybsiAPIEnum


@document_enum
class CybsiLangErrorCodes(CybsiAPIEnum):
    """Stored query error code."""

    InvalidCharacter = "InvalidCharacter"
    """Symbol error: invalid character"""
    InvalidEscapeSequence = "InvalidEscapeSequence"
    """Symbol error: invalid escape sequence"""
    CommentNotTerminated = "CommentNotTerminated"
    """Syntax error: comment not terminated"""
    InvalidNumber = "InvalidNumber"
    """Syntax error: invalid number"""
    StringNotTerminated = "StringNotTerminated"
    """Syntax error: string not terminated"""

    UnexpectedToken = "UnexpectedToken"
    """Syntax error: unexpected token"""

    AmbiguousIdentifierType = "AmbiguousIdentifierType"
    """Semantic error: the identifier has multiple possible types"""
    AttributeNotFound = "AttributeNotFound"
    """Semantic error: attribute not found"""
    DatasourceNotFound = "DatasourceNotFound"
    """Semantic error: datasource not found"""
    DatasourceTypeNotFound = "DatasourceTypeNotFound"
    """Semantic error: datasource type not found"""
    DuplicatedSpecifier = "DuplicatedSpecifier"
    """Semantic error: duplicated specifier"""
    EmptyEntityBody = "EmptyEntityBody"
    """Semantic error: entity has empty body"""
    EmptyExpressionResult = "EmptyExpressionResult"
    """Semantic error: expression produces empty result"""
    EntityTypeNotFound = "EntityTypeNotFound"
    """Semantic error: entity type not found"""
    NoValidRelations = "NoValidRelations"
    """Semantic error: allowed relations for such source and target not found"""
    InvalidOperation = "InvalidOperation"
    """Semantic error: operation is invalid for provided types"""
    InvalidValue = "InvalidValue"
    """Semantic error: value is invalid"""
    InvalidValueType = "InvalidValueType"
    """Semantic error: value type is invalid"""
    RelationKindNotFound = "RelationKindNotFound"
    """Semantic error: relation kind not found"""
    UnsupportedAttribute = "UnsupportedAttribute"
    """Semantic error: attribute is not supported"""

    UnsupportedExpression = "UnsupportedExpression"
    """The expression is allowed by grammar but not supported yet."""
