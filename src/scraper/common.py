"""Useful functions for all the scraper types"""

import gzip
import json
import logging
import re
from pathlib import Path
from typing import Callable
from urllib import parse

import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup, Tag

from time import sleep

CACHE_DIR = Path(__file__).parent.parent.parent / "cache"


def normalize_text(text: str) -> str:
    """Normalize the given text."""
    if text is None:
        return ""
    # Note: amongst other things, this replaces non-breaking spaces
    return re.sub(r"\s+", " ", text.strip())


def resolve_url(url: str, base_url: str) -> str:
    """Resolve the given URL against the given base URL."""
    return parse.urljoin(base_url, url)


def get_cache_path_for_url(url: str, ext: str = "html") -> Path:
    """Get the cache path for the given url."""
    host = parse.urlparse(url).hostname
    assert host is not None
    Path(CACHE_DIR / host).mkdir(parents=True, exist_ok=True)
    quoted = parse.quote(url, "")
    return CACHE_DIR / host / f"{quoted}.{ext}.gz" # / operator concatenates paths


def _fetch(url: str, cache_path: Path, useCache: bool = True) -> str:
    """Fetch the contents of the given URL."""
    # if course is already in cache, return it
    if useCache and cache_path.exists():
        logging.info(f"Getting cached {url}")
        with gzip.open(cache_path, "rt", encoding="utf-8") as _fh:
            return _fh.read()

    # fetch url
    logging.info(f"Requesting {url}")
    response = requests.get(url)
    response.raise_for_status() # check for http error

    # compress text and write to cache
    with gzip.open(cache_path, "wt", encoding="utf-8") as _fh:
        _fh.write(response.text)

    return response.text


def fetch_soup(url: str, useCache: bool = True) -> Tag:
    """Fetch the contents of the given URL and parse as HTML."""
    print("URL:", url)
    cache_path = get_cache_path_for_url(url, ext="html")
    response_text = _fetch(url, cache_path, useCache)
    return BeautifulSoup(response_text, "lxml")


def fetch_soup_retries(url: str, useCache: bool = True, retryWait: int = 5, numRetries: int = 3, exponentialBackoff: bool = False) -> Tag:
    """Fetch soup but wait and retry on HTTPErrors to avoid rate-limiting"""
    for i in range(numRetries):
        try:
            soup = fetch_soup(url, useCache)
            return soup
        except HTTPError:
            logging.info(f"Failed to get url: {url} on attempt {i+1}")
            if i == numRetries - 1: continue # don't wait if this was last attempt
            if exponentialBackoff:
                sleep(retryWait ** (i+1))
            else:
                sleep(retryWait)
            continue
    logging.error(f"Max retires reached for url: {url}")


def fetch_json(url: str) -> dict:
    """Fetch the contents of the given URL and parse as JSON."""
    cache_path = get_cache_path_for_url(url, ext="json")
    response_text = _fetch(url, cache_path)
    return json.loads(response_text)


def get_field_from_soup(el: Tag, op: str | Callable) -> str:
    """Extract normalized text from element based on selector str or function"""
    # if op is a str, use it as a selector str
    if isinstance(op, str):
        elem = el.select_one(op)
        # error if couldn't find anything
        if elem is None:
            raise ValueError(f"Could not find '{op}' in '{el}'")
        return normalize_text(elem.text)

    # if op is a callable, call it and pass the element
    return normalize_text(op(el))
