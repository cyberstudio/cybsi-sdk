"""
A set of utility functions allowing to convert
a string to a valid value of a chosen type.
"""
from cybsi_sdk import enums
from typing import Any, Callable, Dict


_entity_key_converters: Dict[enums.EntityKeyTypes, Callable[[str], Any]] = {
    enums.EntityKeyTypes.String:    str,
    enums.EntityKeyTypes.MD5:       str,
    enums.EntityKeyTypes.SHA1:      str,
    enums.EntityKeyTypes.SHA256:    str,
    enums.EntityKeyTypes.IANAID:    int,
    enums.EntityKeyTypes.NICHandle: str,
    enums.EntityKeyTypes.RIPEID:    str,
}


def convert_entity_key(k_type: enums.EntityKeyTypes, val: str) -> Any:
    """Convert value to entity key type

    :param k_type: type of entity key
    :param val: value to convert
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


def _bool_converter(val: str):
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    raise ValueError("bool value must be 'true' or 'false'")


_attr_value_converters: Dict[enums.AttributeNames, Callable[[str], Any]] = {
    enums.AttributeNames.Size:                  int,
    enums.AttributeNames.Class:                 str,
    enums.AttributeNames.Sectors:               str,
    enums.AttributeNames.DisplayNames:          str,
    enums.AttributeNames.Names:                 str,
    enums.AttributeNames.NodeRoles:             str,
    enums.AttributeNames.MalwareFamilyAliases:  str,
    enums.AttributeNames.IsIoC:                 _bool_converter,
    enums.AttributeNames.IsTrusted:             _bool_converter,
    enums.AttributeNames.IsMalicious:           _bool_converter,
    enums.AttributeNames.IsDGA:                 _bool_converter,
}


def convert_attribute_value(
     attribute_name: enums.AttributeNames,
     val: str) -> Any:
    """Convert value to attribute value type

    :param attribute_name: attribute name
    :param val: string to convert
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
