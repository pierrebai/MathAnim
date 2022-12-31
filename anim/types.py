from typing import Dict as _Dict, Any as _Any, List as _List, Callable as _Callable


#################################################################
#
# Types

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


#################################################################
#
# Lists

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

def last_of(var: _List[_Any]) -> _Any:
    """
    Return the last element of a list of lists of lists...
    """
    if not var:
        return None
    if isinstance(var, list) or isinstance(var, tuple):
        return last_of(var[-1])
    return var
    
def transpose_lists(list_of_lists: _List[list]) -> _List[list]:
    """
    Creates a list of lists by assembling every ith elements of the input lists together in the ith output list.
    This assumes all input lists contain the same number of elements.
    """
    if not list_of_lists:
        return []
    outer_count = len(list_of_lists)
    inner_count = len(list_of_lists[0])
    return [[list_of_lists[outer][inner] for outer in range(outer_count)] for inner in range(inner_count)]

def interleave_lists(list_of_lists: _List[_List[_Any]]) -> _List[_Any]:
    """
    Create a list containing the items from each input list so that
    each nth items from each list are next to each others.
    The shortest list length is used.
    """
    if not list_of_lists:
        return []
    interleaved = []
    for items in zip(*list_of_lists):
        interleaved.extend(items)
    return interleaved


#################################################################
#
# Deep transformations

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

