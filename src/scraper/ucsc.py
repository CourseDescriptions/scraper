from scraper.common import fetch_soup

BASE_LINK = "https://catalog.ucsc.edu"

class UcscScraper:
    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def get_department_urls(self) -> list[str]:
        """Get the urls for each department course page"""
        soup = fetch_soup(BASE_LINK + "/en/2023-2024/general-catalog/courses/")
        main = soup.select_one("#main")
        courseList = main.select_one(".sc-child-item-links")
        courseElems = courseList.select("li")
        return [BASE_LINK + elem.select_one("a")["href"] for elem in courseElems]

    def get_courses(self, url: str) -> list[dict]:
        soup = fetch_soup(url)
        courseList = soup.select_one(".courselist")
        names = courseList.select(".course-name")

        data = []
        for name in names:
            code = name.select_one("span").text.strip()
            title = name.select_one("a").text.replace(code, "").strip()
            desc = name.findNextSibling("div").text.strip()

            course = {
                "code": code,
                "title": title,
                "description": desc,
                "url": url,
            }
            data.append(course)

        return data

    def get(self, useCache: bool, limit: int | None = None) -> list[dict]:
        coursePageUrls = self.get_department_urls()

        data = []

        for page in coursePageUrls:
            data.extend(self.get_courses(page))

        return data