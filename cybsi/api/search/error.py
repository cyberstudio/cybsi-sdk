from enum import Enum

from enum_tools.documentation import document_enum


@document_enum
class CybsiLangErrorCodes(Enum):
    """Stored query error code."""

    # fmt: off
    InvalidCharacter = "InvalidCharacter"  # doc: Symbol error: invalid character
    InvalidEscapeSequence = "InvalidEscapeSequence"  # noqa: E501 doc: Symbol error: invalid escape sequence
    CommentNotTerminated = "CommentNotTerminated"  # noqa: E501 doc: Syntax error: comment not terminated
    InvalidNumber = "InvalidNumber"  # doc: Syntax error: invalid number
    StringNotTerminated = "StringNotTerminated"  # noqa: E501 doc: Syntax error: string not terminated

    UnexpectedToken = "UnexpectedToken"  # doc: Syntax error: unexpected token

    AmbiguousIdentifierType = "AmbiguousIdentifierType"  # noqa: E501 doc: Semantic error: the identifier has multiple possible types
    AttributeNotFound = "AttributeNotFound"  # doc: Semantic error: attribute not found
    DatasourceNotFound = "DatasourceNotFound"  # noqa: E501 doc: Semantic error: datasource not found
    DatasourceTypeNotFound = "DatasourceTypeNotFound"  # noqa: E501 doc: Semantic error: datasource type not found
    DuplicatedSpecifier = "DuplicatedSpecifier"  # noqa: E501 doc: Semantic error: duplicated specifier
    EmptyEntityBody = "EmptyEntityBody"  # doc: Semantic error: entity has empty body
    EmptyExpressionResult = "EmptyExpressionResult"  # noqa: E501 doc: Semantic error: expression produces empty result
    EntityTypeNotFound = "EntityTypeNotFound"  # noqa: E501 doc: Semantic error: entity type not found
    InvalidExpressionScope = "InvalidExpressionScope"  # noqa: E501 doc: Semantic error: expression is invalid in parent scope
    InvalidOperation = "InvalidOperation"  # noqa: E501 doc: Semantic error: operation is invalid for provided types
    InvalidValue = "InvalidValue"  # doc: Semantic error: value is invalid
    InvalidValueType = "InvalidValueType"  # doc: Semantic error: value type is invalid
    UnsupportedAttribute = "UnsupportedAttribute"  # noqa: E501 doc: Semantic error: attribute is not supported
    # fmt: on
