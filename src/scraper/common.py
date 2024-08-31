import gzip
import json
import logging
import re
from pathlib import Path
from typing import Callable
from urllib import parse

import requests
from bs4 import BeautifulSoup, Tag

from scraper.config import CACHE_DIR


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
    return CACHE_DIR / host / f"{quoted}.{ext}.gz"


def _fetch(url: str, cache_path: Path) -> str:
    """Fetch the contents of the given URL."""
    if cache_path.exists():
        with gzip.open(cache_path, "rt") as _fh:
            return _fh.read()

    logging.info(f"Fetching {url}...")
    response = requests.get(url)
    response.raise_for_status()

    with gzip.open(cache_path, "wt") as _fh:
        _fh.write(response.text)

    return response.text


def fetch_soup(url: str) -> Tag:
    """Fetch the contents of the given URL and parse as HTML."""
    cache_path = get_cache_path_for_url(url, ext="html")
    response_text = _fetch(url, cache_path)
    return BeautifulSoup(response_text, "lxml")


def fetch_json(url: str) -> dict:
    """Fetch the contents of the given URL and parse as JSON."""
    cache_path = get_cache_path_for_url(url, ext="json")
    response_text = _fetch(url, cache_path)
    return json.loads(response_text)


def get_field_from_soup(el: Tag, op: str | Callable) -> str:
    if isinstance(op, str):
        elem = el.select_one(op)
        if elem is None:
            # logging.warning(f"Could not find '{field_name}' in '{url}'")
            raise ValueError
        return normalize_text(elem.text)

    return normalize_text(op(el))
