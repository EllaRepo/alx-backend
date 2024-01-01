#!/usr/bin/env python3
"""Module that defines a function that takes two integer arguments page
   and page_size and return a tuple of size two containing a start index
   and an end index corresponding to the range of indexes to return in a
   list for those particular pagination parameters
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """A function that takes two args and returns tuple
    Args:
        page(int): a number
        page_size(int): a number
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
