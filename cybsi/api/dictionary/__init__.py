"""Use this section of API to operate dictionaries and their items.
    Dictionary item is a fact value about certain entity attribute types.
    Use :meth:`cybsi.api.observation.generic.GenericObservationForm.add_attribute_fact`
    to add items to dictionary.
"""

from .api import (
    DictionariesAPI,
    DictionaryView,
    DictionaryItemView,
    DictionaryCommonItemView,
    DictItemAttributeValue,
)
