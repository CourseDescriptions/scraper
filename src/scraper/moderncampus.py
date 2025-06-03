import logging
logger = logging.getLogger(__name__)
from time import sleep
from typing import Tuple

from bs4 import Tag

from scraper.common import (
    fetch_soup,
    fetch_soup_retries,
    get_field_from_soup,
    normalize_text,
    resolve_url,
)

DATA_EXTRACT_NUM_RETRIES = 2
DATA_EXTRACT_SLEEP_SECS = 3

def extract(el):
    start = el.select_one("#course_preview_title ~ hr")

    content = []

    # The Modern Campus sites have unstructured free-form HTML for the course
    #  descriptions.  This heuristic grabs everything from the <hr> under the
    #  title (which *does* seem to be consistent) up until either the next <hr>
    #  (which consistently indicates the end of the block) or the first <strong>
    #  element, which generally seems to introduce the first of (potentially) a
    #  bunch of additional metadata which is not part of the description itself.
    #  Other tags are passed over.
    # This is far from perfect, but it will have to do for now.
    for sibling in start.next_siblings:
        if sibling.name == "hr":
            break

        if sibling.name == "strong":
            break

        if sibling.name:
            continue

        content.append(sibling)

    return normalize_text(" ".join(content))


class ModernCampusScraper:
    """Course Descriptions Scraper for "Modern Campus"-type sites."""

    def __init__(self, site_config: dict) -> None:
        """
        config format: {
            "startUrl": string url to all courses list page of catalog
                        (look at other configs for example of which page)
            "selectors": {
                "code": selector for course code
                "title": selector for course title
                [OPTIONAL] "description": selector for course description
                                          (defaults to extract() function)
            }
        }
        Selectors can be either strings, and will be treated as a css selector
        Or they can be a function that returns a string, 
        in which case the function will be called on the soup of the page
        """
        self.config = site_config

    def extract_data_from_course_page_url(self, url: str, useCache: bool = True) -> dict | None:
        """Extract information from the given course page."""
        soup = fetch_soup_retries(url, useCache)

        # Do this with the fetch retry instead probably? Or at least add delay
        for i in range(DATA_EXTRACT_NUM_RETRIES):
            try:
                data = {
                    "code": get_field_from_soup(soup, self.config["selectors"].get("code")),
                    "title": get_field_from_soup(soup, self.config["selectors"].get("title")),
                    "description": get_field_from_soup(soup, self.config["selectors"].get("description"))\
                        if "description" in self.config["selectors"] else extract(soup),
                    "url": url,
                }
                return data
            except Exception as e:
                if i == DATA_EXTRACT_NUM_RETRIES - 1: continue # if last loop don't sleep
                logger.info(f"Encountered error {e} while extracting data from {url}...\
                            sleeping 3 and then trying to refetch")
                sleep(DATA_EXTRACT_SLEEP_SECS)
                continue

        logger.error(f"Failed while extracting data from {url}, continuing")
        return None

    def extract_urls_from_catalog_page_soup(self, soup: Tag) -> list[Tuple[str, str]]:
        # consider using /ajax/preview_course.php?catoid=35&coid=143860&show pages
        #   instead of /preview_course_nopop.php?catoid=35&coid=143860 ??
        # nb. these are not the same, and the "preview_course" versions look less
        #     regular and harder to parse (at first glance, at least).
        return [
            (
                normalize_text(el.text),
                resolve_url(el.attrs["href"], self.config["startUrl"]),
            )
            for el in soup.select("a[href^='preview_course_nopop.php']")
        ]

    def get(self, useCache: bool = True, limit: int | None = None) -> list[dict]:
        """Get course descriptions for all subject codes."""

        soup = fetch_soup(self.config["startUrl"], useCache)
        current_page = getattr(soup.select_one("[aria-current=page]"), "text", None)
        last_page = getattr(
            soup.select_one("[aria-current=page] ~ a:last-child"), "text", None
        )

        if current_page is None or last_page is None:
            raise Exception("Could not determine number of catalog pages -- aborting")

        logger.debug("%s catalog pages found", last_page)

        urls = self.extract_urls_from_catalog_page_soup(soup)

        for i in range(2, int(last_page) + 1):
            soup = fetch_soup(self.config["startUrl"] + f"&filter[cpage]={i}", useCache)
            current_page = getattr(soup.select_one("[aria-current=page]"), "text", None)
            # if this assert fails, may be because page did not load successfully (Fresno_State...)
            try:
                assert current_page == str(i)
            except AssertionError as e:
                logger.error(f"Though current_page would be {i}, was {current_page}\nWaiting 5s and then refetching")
                sleep(5)
                soup = fetch_soup(self.config["startUrl"] + f"&filter[cpage]={i}", False)
                current_page = getattr(soup.select_one("[aria-current=page]"), "text", None)
                assert current_page == str(i)

            urls += self.extract_urls_from_catalog_page_soup(soup)
            
            # if we've got more urls than limit, ignore and cap urls
            if (limit and len(urls) >= limit):
                urls = urls[:limit]
                break

        logger.debug("%d course pages found", len(urls))

        data = [self.extract_data_from_course_page_url(url, useCache) for _title, url in urls]
        data = [course for course in data if course] # remove null courses from failed scrapes

        return data

    def get_author(self) -> str:
        return "Simon Wiles"