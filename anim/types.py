from typing import Dict as _Dict, Any as _Any, List as _List, Callable as _Callable

def is_of_type(var, type) -> bool:
    """
    Verifies if a variable is of the given type or is a list or tuple of that type
    of a list of list of that type, etc.
    """
    if ( isinstance(var, list) or isinstance(var, tuple) ) and len(var):
        for item in var:
            if is_of_type(item, type):
                return True
        return False
    else:
        return isinstance(var, type)

def flatten(var) -> _List[_Any]:
    """
    Flatten a potentially recursive list or tuple of list or tuple,
    until what we have is a simple flat list.
    """
    items = []
    if isinstance(var, list) or isinstance(var, tuple):
        for item in var:
            items.extend(flatten(item))
    else:
        items.append(var)
    return items

def deep_map(mapping: _Callable, *args):
    """
    Recurse on all lists of lists to map all non-list items.
    The results will have the same list-of-lists structure.
    Also support tuples.
    """
    if not args:
        return None
    if isinstance(args[0], list):
        return [deep_map(mapping, *items) for items in zip(*args)]
    elif isinstance(args[0], tuple):
        return tuple([deep_map(mapping, *items) for items in zip(*args)])
    else:
        return mapping(*args)

def deep_filter(filtering: _Callable, *args):
    """
    Recurse on all lists of lists to filter all non-list items.
    The results will have the same list-of-lists structure.
    Also support tuples.
    """
    if not args:
        return None
    if isinstance(args[0], list):
        return list(filter(lambda x: x is not None, [deep_filter(filtering, *items) for items in zip(*args)]))
    elif isinstance(args[0], tuple):
        return tuple(filter(lambda x: x is not None, [deep_filter(filtering, *items) for items in zip(*args)]))
    else:
        return filtering(*args)

def find_all_of_type(module_dict: _Dict[str, _Any], type, ignore_private: bool = True) -> list:
    """
    Finds all global variable containing value of the given type.
    Return the list of such values.
    """
    values = []
    for var_name, var in module_dict.items():
        if ignore_private and var_name.startswith('_'):
            continue
        if not is_of_type(var, type):
            continue
        values.extend(flatten(var))
    return values
