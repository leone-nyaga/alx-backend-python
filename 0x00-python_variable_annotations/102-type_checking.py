#!/usr/bin/env python3
"""Type Checking"""
from typing import Tuple, List, Any, Union


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """type checking"""
    zoomed_in: List = [
        item for item in lst for i in range(factor)
    ]
    return zoomed_in
