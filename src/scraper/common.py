import gzip
import logging
import re
from pathlib import Path
from typing import Callable
from urllib import parse

import requests
from bs4 import Tag

from scraper.config import CACHE_DIR


def normalize_text(text: str) -> str:
    """Normalize the given text."""
    # Note: amongst other things, this replaces non-breaking spaces
    return re.sub(r"\s+", " ", text.strip())


def resolve_url(url: str, base_url: str) -> str:
    """Resolve the given URL against the given base URL."""
    return parse.urljoin(base_url, url)


def get_cache_path_for_url(url: str) -> Path:
    """Get the cache path for the given url."""
    quoted = parse.quote(url, "")
    return CACHE_DIR / f"{quoted}.html.gz"


def fetch(url: str) -> str:
    """Fetch the contents of the given URL."""
    cache_path = get_cache_path_for_url(url)
    if cache_path.exists():
        with gzip.open(cache_path, "rt") as _fh:
            return _fh.read()

    logging.info(f"Fetching {url}...")
    response = requests.get(url)
    response.raise_for_status()

    with gzip.open(cache_path, "wt") as _fh:
        _fh.write(response.text)

    return response.text


def get_field_from_soup(el: Tag, op: str | Callable) -> str:
    if isinstance(op, str):
        elem = el.select_one(op)
        if elem is None:
            # logging.warning(f"Could not find '{field_name}' in '{url}'")
            raise ValueError
        return normalize_text(elem.text)

    return normalize_text(op(el))
