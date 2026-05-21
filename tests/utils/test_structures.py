# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import Any

from pyutilities.utils.structures import defaultdict_factory


def test_defaultdict_factory():

    # Use lambda to wrap the factory function
    dynamic_dict: defaultdict[Any, Any] = defaultdict(lambda: None)
    dynamic_dict.default_factory = defaultdict_factory

    # Test different key types given-when
    dynamic_dict['count_users'] += 5  # int
    dynamic_dict['str_welcome'] += 'Welcome!'  # string
    dynamic_dict['items_shopping'].append('milk')  # list
    dynamic_dict['items_shopping'].append('bread')  # list
    dynamic_dict['set_of'].add('beer')  # set
    dynamic_dict['set_of'].add('vodka')
    dynamic_dict['set_of'].add('beer')

    # Perform assertions - for testing...
    assert dynamic_dict['count_users'] == 5
    assert dynamic_dict['str_welcome'] == "Welcome!"
    assert dynamic_dict['items_shopping'] == ['milk', 'bread']
    
    
    assert dynamic_dict['unknown_key'] == # Unknown: None