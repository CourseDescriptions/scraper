#!/usr/bin/env python3

"""Course Descriptions Scraper for "squares"-type sites."""

__version__ = "0.1"

import logging
import re
from typing import Tuple
from pathlib import Path
from urllib import parse

import requests
import typer
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.logging import RichHandler

from scraper.config import SITES, CACHE_DIR

cli = typer.Typer(add_completion=False, no_args_is_help=True)


def normalize_text(text: str) -> str:
    """Normalize the given text."""
    # Note: amongst other things, this replaces non-breaking spaces
    return re.sub(r"\s+", " ", text.strip())


def get_cache_path_for_url(url: str) -> Path:
    """Get the cache path for the given url."""
    quoted = parse.quote(url, "")
    return CACHE_DIR / f"{quoted}.html"


def fetch(url: str) -> str:
    """Fetch the contents of the given URL."""
    cache_path = get_cache_path_for_url(url)
    if cache_path.exists():
        with cache_path.open() as _fh:
            return _fh.read()

    logging.info(f"Fetching {url}...")
    response = requests.get(url)
    response.raise_for_status()

    with cache_path.open("w") as _fh:
        _fh.write(response.text)

    return response.text


class SquaresScraper:
    """Course Descriptions Scraper for "squares"-type sites."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def extract_subject_code_pages(self) -> list[Tuple[str, str]]:
        """Extract a list of subject code pages from the given HTML."""
        html = fetch(self.config["subjectCodesUrl"])
        soup = BeautifulSoup(html, "html.parser")
        return [
            (
                el.text,
                el.attrs["href"]
                if el.attrs["href"].startswith("http")
                else self.config["urlBase"] + el.attrs["href"],
            )
            for el in soup.select(".letternav-head + ul li a")
        ]

    def extract_from_subject_code_page(self, url: str) -> list[dict]:
        """Extract information from the given subject code page."""
        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        def get_text(field_name: str) -> str:
            op = self.config["selectors"].get(field_name)
            if type(op) is str:
                elem = el.select_one(op)
                if elem is None:
                    logging.warning(f"Could not find '{field_name}' in '{url}'")
                    raise ValueError
                return normalize_text(elem.text)

            return normalize_text(op(el))

        data = []
        for el in soup.select(".courseblock"):
            code = get_text("code")
            title = get_text("title")
            description = get_text("description")
            data.append({"code": code, "title": title, "description": description})

        return data


@cli.callback()
def common_options(
    verbose: bool = typer.Option(False, "--verbose", "-v"),
    quiet: bool = typer.Option(False, "--quiet", "-q"),
    version: bool = typer.Option(False, "--version"),
):
    """Common options:"""

    if version:
        print(__version__)
        raise SystemExit

    log_level = logging.DEBUG if verbose else logging.INFO
    log_level = logging.CRITICAL if quiet else log_level
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(markup=False, console=Console(width=180))],
    )


@cli.command()
def go():
    scraper = SquaresScraper(SITES["UC_Davis"])
    subject_code_pages = scraper.extract_subject_code_pages()

    for _title, url in subject_code_pages[:1]:
        data = scraper.extract_from_subject_code_page(url)
        print(data)


if __name__ == "__main__":
    cli()
