#!/usr/bin/env python3
"""Module that defines a function that takes two integer arguments page
   and page_size and return a tuple of size two containing a start index
   and an end index corresponding to the range of indexes to return in a
   list for those particular pagination parameters
"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple:
    """A function that takes two args and returns tuple
    Args:
        page(int): a number
        page_size(int): a number
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        """
        page_assert = "Page must be an integer greater than 0"
        page_sz_assert = "Page size must be an integer greater than 0"
        assert isinstance(page, int) and page > 0, page_assert
        assert isinstance(page_size, int) and page_size > 0, page_sz_assert

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)
        if start_index >= len(dataset):
            return []
        return dataset[start_index:end_index]
