#!/usr/bin/env python3
"""BaseCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class
    """
    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item value
           for the key key
        Args:
            key - a key
            item - an item
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

    def get(self, key):
        """return the value in self.cache_data linked to key
        Args:
            key - a key
        Returns:
            returns a value
        """
        if key is not None:
            return self.cache_data.get(key)
        else:
            return None
