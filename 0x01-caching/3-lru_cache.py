#!/usr/bin/env python3
"""LRUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """LRUCache class
    """
    def __init__(self):
        """Initialization
        """
        self.lru = []
        super().__init__()

    def put(self, key, item):
        """Assign to the dictionary self.cache_data the item value
           for the key key
        Args:
            key - a key
            item - an item
        """
        if key is not None and item is not None:
            ln = len(self.cache_data)
            if ln >= BaseCaching.MAX_ITEMS and key not in self.cache_data:
                print("DISCARD: {}".format(self.lru[0]))
                del self.cache_data[self.lru[0]]
                del self.lru[0]
            if key in self.cache_data:
                del self.lru[self.lru.index(key)]
            self.lru.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Return the value in self.cache_data linked to key
        Args:
            key - a key
        Returns:
            returns a value
        """
        if key is not None and key in self.cache_data.keys():
            del self.lru[self.lru.index(key)]
            self.lru.append(key)
            return self.cache_data.get(key)
        else:
            return None
