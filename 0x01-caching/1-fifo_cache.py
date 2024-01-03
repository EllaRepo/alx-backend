#!/usr/bin/env python3
"""FIFOCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """FIFOCache class
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
                    first_key = next(iter(self.cache_data))
                    del self.cache_data[first_key]
                    print("DISCARD: {}".format(first_key))
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
