import logging
from typing import Tuple

from scraper.common import fetch_soup, get_field_from_soup, resolve_url


class CourseLeafScraper:
    """Course Descriptions Scraper for "squares"-type sites."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def extract_subject_code_pages(self) -> list[Tuple[str, str]]:
        """Extract a list of subject code pages from the given HTML."""
        soup = fetch_soup(self.config["subjectCodesUrl"])
        return [
            (
                el.text,
                resolve_url(el.attrs["href"], self.config["subjectCodesUrl"]),
            )
            for el in soup.select(".letternav-head + ul li a")
        ]

    def extract_from_subject_code_page_url(self, url: str) -> list[dict]:
        """Extract information from the given subject code page."""
        soup = fetch_soup(url)

        try:
            data = [
                {
                    **{
                        field: get_field_from_soup(
                            el, self.config["selectors"].get(field)
                        )
                        for field in ["code", "title", "description"]
                    },
                    **{"url": url},
                }
                for el in soup.select(".courseblock")
            ]
        except ValueError as e:
            logging.fatal("Could not extract data from %s", url)
            logging.fatal(e)
            raise SystemExit(1) from None

        return data

    def get(self, limit: int | None = None) -> list[dict]:
        """Get course descriptions for all subject codes."""
        subject_code_pages = self.extract_subject_code_pages()

        if limit is not None:
            subject_code_pages = subject_code_pages[:limit]

        data = [
            course_data
            for _title, url in subject_code_pages
            for course_data in self.extract_from_subject_code_page_url(url)
        ]

        return data
