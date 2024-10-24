#!/usr/bin/env python3
"""
File: web.py

Implements an expiring web cache and tracker
"""
from functools import wraps
from typing import Callable
import requests
import redis


def cache_result(function: Callable) -> Callable:
    """
    A decorator that implements an expiring to a web cache and
    tracks number of time a particular URL was accessed.
    """
    @wraps(function)
    def wrapper(url):
        """ Wrapper """
        client = redis.Redis()

        # Cache content
        key = "content:" + url
        cached_content = client.get(key)
        if cached_content:
            return cached_content.decode("utf-8")

        # Updated cache content
        key_count = "count:" + url
        client.incr(key_count)
        html = function(url)
        client.set(key, html, ex=10)

        return html
    return wrapper


@cache_result
def get_page(url: str) -> str:
    """
    parameters:
    - url (url): A url to simulate slow response

    Returns:
    - (str): Content of a particular URL.
    """
    response = requests.get(url)
    return response.text
