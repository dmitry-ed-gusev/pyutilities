# -*- coding: utf-8 -*-

from pyutilities.utils.structures import KeyAwareDefaultDict


def test_defaultdict_factory():

    # Use lambda to wrap the factory function
    dynamic_dict = KeyAwareDefaultDict()

    # Test different key types given-when - data + assertions
    dynamic_dict['count_users'] += 5  # int
    dynamic_dict['count_users'] += 6  # int
    assert dynamic_dict['count_users'] == 11

    dynamic_dict['str_welcome'] += 'Welcome!'  # string
    dynamic_dict['str_welcome'] += ' Have a nice day!'  # string
    assert dynamic_dict['str_welcome'] == "Welcome! Have a nice day!"

    dynamic_dict['items_shopping'].append('milk')  # list
    dynamic_dict['items_shopping'].append('bread')  # list
    dynamic_dict['items_shopping'].append(['one', 'two'])  # list
    assert dynamic_dict['items_shopping'] == ['milk', 'bread', ['one', 'two']]

    dynamic_dict['set_of'].add('beer')  # set
    dynamic_dict['set_of'].add('vodka')  # set
    dynamic_dict['set_of'].add('beer')  # set (duplicate, should not be added)
    dynamic_dict['set_of'].add('vodka')  # set (duplicate, should not be added)
    dynamic_dict['set_of'].add('')  # set
    dynamic_dict['set_of'].add(None)  # set
    dynamic_dict['set_of'].add(None)  # set
    assert dynamic_dict['set_of'] == {'beer', 'vodka', '', None}

    dynamic_dict['dict_user'] = {'name': 'Alice', 'age': 30}  # dict
    dynamic_dict['dict_user']['city'] = 'New York'  # dict
    assert dynamic_dict['dict_user'] == {'name': 'Alice', 'age': 30, 'city': 'New York'}

    # check for an unknown key that does not match any prefix
    assert dynamic_dict['unknown_key'] is None  # unknown key, should return None
