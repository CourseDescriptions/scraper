from scraper.common import fetch_soup

BASE_LINK = "https://catalog.ucsd.edu"

class UCSDScraper:
    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def get_department_urls(self) -> list[str]:
        soup = fetch_soup(BASE_LINK + "/front/courses.html")
        links = soup.find_all("a")
        # get all the hrefs for courses (all formatted as "../courses/CS.html")
        # and add them to base link to get correct absolute url
        return [BASE_LINK + link["href"][2:] for link in links if link.text=="courses"]

    def get_courses(self, url: str) -> list[dict]:
        return []

    def get(self, useCache: bool, limit: int | None = None) -> list[dict]:
        coursePageUrls = self.get_department_urls()

        print("URLS:", coursePageUrls)

        data = []

        return data


def get_config(): return {
  "name": "UC San Francisco",
  "type": UCSDScraper,
}