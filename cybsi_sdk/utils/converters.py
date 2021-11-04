"""
A set of utility functions allowing to convert
a string to a valid value of a chosen type.
"""
from cybsi_sdk import enums
from typing import Any, Callable, Dict


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


_entity_key_converters: Dict[enums.EntityKeyTypes, Callable[[Any], Any]] = {
    enums.EntityKeyTypes.String:    _str_converter,
    enums.EntityKeyTypes.MD5:       _str_converter,
    enums.EntityKeyTypes.SHA1:      _str_converter,
    enums.EntityKeyTypes.SHA256:    _str_converter,
    enums.EntityKeyTypes.IANAID:    _str_converter,
    enums.EntityKeyTypes.NICHandle: _str_converter,
    enums.EntityKeyTypes.RIPEID:    _str_converter,
}


def convert_entity_key(k_type: enums.EntityKeyTypes, val: Any) -> Any:
    """Convert value to entity key type

    :param k_type: type of entity key
    :param val: value to convert.
        Usually string, but value of desired type is accepted too
    :return: valid value of entity key, return type depends on entity key type
    """

    converter = _entity_key_converters.get(k_type)
    if not converter:
        raise ValueError("no converter for key type: %s", k_type)
    try:
        result = converter(val)
    except ValueError:
        raise ValueError(f'"{val}" is not convertible to {k_type} value')
    return result


_attr_value_converters: Dict[enums.AttributeNames, Callable[[str], Any]] = {
    enums.AttributeNames.Size:                  _int_converter,
    enums.AttributeNames.Class:                 _str_converter,
    enums.AttributeNames.Sectors:               _str_converter,
    enums.AttributeNames.DisplayNames:          _str_converter,
    enums.AttributeNames.Names:                 _str_converter,
    enums.AttributeNames.NodeRoles:             _str_converter,
    enums.AttributeNames.MalwareFamilyAliases:  _str_converter,
    enums.AttributeNames.IsIoC:                 _bool_converter,
    enums.AttributeNames.IsTrusted:             _bool_converter,
    enums.AttributeNames.IsMalicious:           _bool_converter,
    enums.AttributeNames.IsDGA:                 _bool_converter,
}


def convert_attribute_value(
     attribute_name: enums.AttributeNames,
     val: Any) -> Any:
    """Convert value to attribute value type

    :param attribute_name: attribute name
    :param val: value to convert.
        Usually string, but value of desired type is accepted too
    :return: valid value of attribute, return type depends on attribute
    """

    converter = _attr_value_converters.get(attribute_name)
    if not converter:
        raise ValueError("no converter for attribute: %s", attribute_name)
    try:
        result = converter(val)
    except ValueError:
        raise ValueError(
            f'"{val}" is not convertible to {attribute_name} value'
        )
    return result
