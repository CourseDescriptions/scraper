import logging
from typing import Tuple

from bs4 import BeautifulSoup
from rich import print

from scraper.common import fetch, normalize_text


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

        def get_text(el: BeautifulSoup, field_name: str) -> str:
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
            code = get_text(el, "code")
            title = get_text(el, "title")
            description = get_text(el, "description")
            data.append({"code": code, "title": title, "description": description})

        return data

    def get(self) -> None:
        """Get course descriptions for all subject codes."""
        # !! FIXME: Currently hard-coded to only the first subject code
        subject_code_pages = self.extract_subject_code_pages()

        for _title, url in subject_code_pages[:1]:
            data = self.extract_from_subject_code_page(url)
            print(data)
