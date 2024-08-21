"""Use this section of API to operate dictionaries and their items.
    Dictionary is an open set of string values. Dictionary items are used
    as attribute values. For example, dictionary "MalwareFamilies" contains names
    of malware families known by system.
    Use :meth:`cybsi.api.observation.generic.GenericObservationForm.add_attribute_fact`
    or :meth:`~DictionariesAPI.register_item()` to add items to a dictionary.
"""

from .api import (
    DictionariesAPI,
    DictionariesAsyncAPI,
    DictionaryItemForm,
    DictionaryView,
    DictionaryCommonView,
    DictionaryItemView,
    DictionaryItemCommonView,
    DictItemAttributeValue,
)
