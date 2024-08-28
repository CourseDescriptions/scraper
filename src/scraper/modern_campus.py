import logging
from typing import Tuple

from bs4 import BeautifulSoup
from rich import print

from scraper.common import (
    fetch,
    get_field_from_soup,
    normalize_text,
    resolve_url,
)


class ModernCampusScraper:
    """Course Descriptions Scraper for "Modern Campus"-type sites."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def extract_data_from_course_page_url(self, url: str) -> dict:
        """Extract information from the given course page."""
        html = fetch(url)
        soup = BeautifulSoup(html, "lxml")

        data = {
            field: get_field_from_soup(soup, self.config["selectors"].get(field))
            for field in ["code", "title", "description"]
        }

        return data

    def extract_urls_from_catalog_page_soup(
        self, soup: BeautifulSoup
    ) -> list[Tuple[str, str]]:
        # consider using /ajax/preview_course.php?catoid=35&coid=143860&show pages
        #   instead of /preview_course_nopop.php?catoid=35&coid=143860 ??
        return [
            (
                normalize_text(el.text),
                resolve_url(el.attrs["href"], self.config["startUrl"]),
            )
            for el in soup.select("a[href^='preview_course_nopop.php']")
        ]

    def get(self) -> None:
        # """Get course descriptions for all subject codes."""

        html = fetch(self.config["startUrl"])
        soup = BeautifulSoup(html, "lxml")
        current_page = soup.select_one("[aria-current=page]").text
        last_page = soup.select_one("[aria-current=page] ~ a:last-child").text

        logging.debug("%s catalog pages found", last_page)

        urls = self.extract_urls_from_catalog_page_soup(soup)

        for i in range(2, int(last_page) + 1):
            html = fetch(self.config["startUrl"] + f"&filter[cpage]={i}")
            soup = BeautifulSoup(html, "lxml")
            current_page = soup.select_one("[aria-current=page]").text
            assert current_page == str(i)

            urls += self.extract_urls_from_catalog_page_soup(soup)

        logging.debug("%d course pages found", len(urls))
        # print(urls)
        # print(len(urls))

        for _title, url in urls[:2]:
            data = self.extract_data_from_course_page_url(url)
            print(data)
