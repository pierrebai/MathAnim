from typing import Dict as _Dict, Any as _Any

def is_of_type(var, type) -> bool:
    """
    Verifies if a variable is of the given type or is a list or tuple of that type
    of a list of list of that type, etc.
    """
    if isinstance(var, list) and len(var):
        return is_of_type(var[0], type)
    elif isinstance(var, tuple) and len(var):
        return is_of_type(var[0], type)
    else:
        return isinstance(var, type)

def flatten(var) -> list:
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
