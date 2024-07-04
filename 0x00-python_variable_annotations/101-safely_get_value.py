#!/usr/bin/env python3
"""
Annotate the below function’s parameters and
return value with the appropriate types
"""

from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any, default:
                     Union[T, None] = None) -> Union[Any, T]:
    """
    Given the parameters and return values, add type
    annotations to the function
    """
    if key in dct:
        return dct[key]
    else:
        return default
