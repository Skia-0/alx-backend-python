#!/usr/bin/env python3
import requests
from functools import wraps

def get_json(url):
    """Simple wrapper to get JSON from a URL"""
    response = requests.get(url)
    return response.json()

def memoize(func):
    """Memoization decorator"""
    cache = {}

    @property
    @wraps(func)
    def wrapper(self):
        if func not in cache:
            cache[func] = func(self)
        return cache[func]
    return wrapper
