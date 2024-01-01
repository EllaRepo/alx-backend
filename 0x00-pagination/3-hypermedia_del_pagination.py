#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Tuple, Dict


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
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """Takes 2 integer arguments and returns a dictionary
        Args:
            index(int): first required index
            page_size(int): required number of records per page
        Returns:
            a dictionary
        """
        msg = "Index must be a positive integer or None"
        assert index is None or (isinstance(index, int) and index >= 0), msg

        dataset = self.indexed_dataset()
        data_length = len(dataset)
        assert index < data_length, "Index is out of range"

        response = {"index": index}
        data = []

        for _ in range(page_size):
            while True:
                curr = dataset.get(index)
                index += 1
                if curr is not None:
                    break
            data.append(curr)

        response['data'] = data
        response['page_size'] = len(data)
        response['next_index'] = index if dataset.get(index) else None

        return response
