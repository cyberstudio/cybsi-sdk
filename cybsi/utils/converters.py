"""
A set of utility functions allowing to convert
a string to a valid value of a chosen type.
"""
from typing import Any, Callable, Dict

from cybsi.api.observable.enums import EntityKeyTypes, AttributeNames


def _str_converter(val: str):
    if isinstance(val, str):
        return val.strip()
    raise ValueError(f"value {val} is not a string")


def _int_converter(val: str):
    return int(val)


def _bool_converter(val: str):
    if isinstance(val, bool):
        return val

    if not isinstance(val, str):
        raise ValueError(f"value {val} is not boolean")

    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    raise ValueError("bool value must be 'true' or 'false'")


_entity_key_converters: Dict[EntityKeyTypes, Callable[[Any], Any]] = {
    EntityKeyTypes.String: _str_converter,
    EntityKeyTypes.MD5: _str_converter,
    EntityKeyTypes.SHA1: _str_converter,
    EntityKeyTypes.SHA256: _str_converter,
    EntityKeyTypes.IANAID: _str_converter,
    EntityKeyTypes.NICHandle: _str_converter,
    EntityKeyTypes.RIPEID: _str_converter,
}


def convert_entity_key(k_type: EntityKeyTypes, val: Any) -> Any:
    """Convert value to entity key type.

    Args:
        k_type: Type of entity key.
        val: Value to convert. Usually string,
         but value of desired type is accepted too.
    Return:
        Valid value of entity key, return type depends on entity key type.
    """

    converter = _entity_key_converters.get(k_type)
    if not converter:
        raise ValueError("no converter for key type: %s", k_type)
    try:
        result = converter(val)
    except ValueError:
        raise ValueError(f'"{val}" is not convertible to {k_type} value')
    return result


_attr_value_converters: Dict[AttributeNames, Callable[[str], Any]] = {
    AttributeNames.Size: _int_converter,
    AttributeNames.Class: _str_converter,
    AttributeNames.Sectors: _str_converter,
    AttributeNames.DisplayNames: _str_converter,
    AttributeNames.Names: _str_converter,
    AttributeNames.NodeRoles: _str_converter,
    AttributeNames.MalwareFamilyAliases: _str_converter,
    AttributeNames.IsIoC: _bool_converter,
    AttributeNames.IsTrusted: _bool_converter,
    AttributeNames.IsMalicious: _bool_converter,
    AttributeNames.IsDGA: _bool_converter,
}


def convert_attribute_value(attribute_name: AttributeNames, val: Any) -> Any:
    """Convert value to attribute value type.

    Args:
        attribute_name: attribute name.
        val: value to convert.
         Usually string, but value of desired type is accepted too.
    Return:
        Valid value of attribute, return type depends on attribute.
    """

    converter = _attr_value_converters.get(attribute_name)
    if not converter:
        raise ValueError("no converter for attribute: %s", attribute_name)
    try:
        result = converter(val)
    except ValueError:
        raise ValueError(
            f'"{val}" is not convertible to {attribute_name} value'
        ) from None
    return result
