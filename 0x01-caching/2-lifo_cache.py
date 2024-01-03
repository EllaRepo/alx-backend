#!/usr/bin/env python3
"""LIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """LIFOCache class
    """
    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item value
           for the key key
        Args:
            key - a key
            item - an item
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                if key not in self.cache_data:
                    first_key = list(self.cache_data.keys())[-1]
                    del self.cache_data[first_key]
                    print("DISCARD: {}".format(first_key))
                else:
                    del self.cache_data[key]
            self.cache_data[key] = item

    def get(self, key):
        """Return the value in self.cache_data linked to key
        Args:
            key - a key
        Returns:
            returns a value
        """
        if key is not None:
            return self.cache_data.get(key)
        else:
            return None
