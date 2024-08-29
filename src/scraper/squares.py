from typing import Tuple

from bs4 import BeautifulSoup

from scraper.common import fetch, get_field_from_soup, resolve_url


class SquaresScraper:
    """Course Descriptions Scraper for "squares"-type sites."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def extract_subject_code_pages(self) -> list[Tuple[str, str]]:
        """Extract a list of subject code pages from the given HTML."""
        html = fetch(self.config["subjectCodesUrl"])
        soup = BeautifulSoup(html, "lxml")
        return [
            (
                el.text,
                resolve_url(el.attrs["href"], self.config["subjectCodesUrl"]),
            )
            for el in soup.select(".letternav-head + ul li a")
        ]

    def extract_from_subject_code_page_url(self, url: str) -> list[dict]:
        """Extract information from the given subject code page."""
        html = fetch(url)
        soup = BeautifulSoup(html, "lxml")

        data = [
            {
                **{
                    field: get_field_from_soup(el, self.config["selectors"].get(field))
                    for field in ["code", "title", "description"]
                },
                **{"url": url},
            }
            for el in soup.select(".courseblock")
        ]

        return data

    def get(self) -> list[dict]:
        """Get course descriptions for all subject codes."""
        subject_code_pages = self.extract_subject_code_pages()

        data = [
            course_data
            for _title, url in subject_code_pages
            for course_data in self.extract_from_subject_code_page_url(url)
        ]

        return data
