#!/usr/bin/env python3
"""LFUCache module
"""
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """LFUCache class
    """
    def __init__(self):
        """Initialization
        """
        self.lfu = {}
        super().__init__()

    def lfu_algo(self):
        lfu_key, lfu_value = None, 0
        for key in self.lfu:
            if lfu_key is None:
                lfu_key = key
                lfu_value = self.lfu[key]
            else:
                if self.lfu[key] < lfu_value:
                    lfu_key = key
                    lfu_value = self.lfu[key]
        return lfu_key

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
                lfu = self.lfu_algo()
                print("DISCARD: {}".format(lfu))
                del self.cache_data[lfu]
                del self.lfu[lfu]
            self.cache_data[key] = item
            if key in self.lfu.keys():
                self.lfu[key] = self.lfu[key] + 1
            else:
                self.lfu[key] = 1

    def get(self, key):
        """Return the value in self.cache_data linked to key
        Args:
            key - a key
        Returns:
            returns a value
        """
        if key is not None and key in self.cache_data.keys():
            if key in self.lfu.keys():
                freq = self.lfu[key]
                del self.lfu[key]
                self.lfu[key] = freq + 1
            else:
                self.lfu[key] = 1
            return self.cache_data.get(key)
        else:
            return None
