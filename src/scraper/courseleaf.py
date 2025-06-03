import logging
logger = logging.getLogger(__name__)

from requests import HTTPError
from typing import Tuple

from scraper.common import fetch_soup, get_field_from_soup, resolve_url


class CourseLeafScraper:
    """Course Descriptions Scraper for "squares"-type sites."""

    def __init__(self, site_config: dict) -> None:
        """
        config format: {
            "subjectCodesUrl": string url to department listing page of catalog
                               (look at other configs for example of which page)
            "selectors": {
                "code": selector for course code
                "title": selector for course title
                "description": selector for course description
            }
        }
        Selectors can be either strings, and will be treated as a css selector
        Or they can be a function that returns a string, 
        in which case the function will be called on the soup of the page
        """
        self.config = site_config

    def extract_subject_code_pages(self, useCache: bool) -> list[Tuple[str, str]]:
        """Extract a list of subject code pages from the given HTML."""
        soup = fetch_soup(self.config["subjectCodesUrl"], useCache)
        code_selector = self.config["subjectCodeSelector"] if "subjectCodeSelector" in self.config else ".letternav-head + ul li a"
        return [
            (
                el.text,
                resolve_url(el.attrs["href"], self.config["subjectCodesUrl"]),
            )
            for el in soup.select(code_selector)
        ]

    def extract_from_subject_code_page_url(self, url: str, useCache: bool) -> list[dict]:
        """Extract information from the given subject code page."""
        try:
            soup = fetch_soup(url, useCache)
        except HTTPError as e:
            logging.error(f"Failed to get subject code page for url {url}, continuing", exc_info=True)
            return []

        try:
            data = [ {
                    **{field: get_field_from_soup(el, self.config["selectors"].get(field))
                        for field in ["code", "title", "description"]},
                    **{"url": url}
                } for el in soup.select(".courseblock")
            ]
        except ValueError as e:
            logger.fatal(f"Could not extract data from {url}", exc_info=True)
            raise SystemExit(1) from None

        for course in data:
            for key, value in course.items():
                if len(value) == 0:
                    logger.warning(f"Field {key} has value of length zero for url {url}")

        return data

    def get(self, useCache: bool = True, limit: int | None = None) -> list[dict]:
        """Get course descriptions for all subject codes."""
        subject_code_pages = self.extract_subject_code_pages(useCache)

        # limit pages of courses we get (so limit=2 gives all courses from first two departments, alphabetically)
        if limit is not None:
            subject_code_pages = subject_code_pages[:limit]

        data = [
            course_data
            for _title, url in subject_code_pages
            for course_data in self.extract_from_subject_code_page_url(url, useCache)
        ]

        return data

    
    def get_author(self):
        return "Simon Wiles"