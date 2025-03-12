from scraper.common import fetch_soup
import logging
from time import sleep

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
        soup = fetch_soup(url)
        courseNames = soup.select(".course-name")
        
        data = []
        for name in courseNames:
            nameText = name.text.strip().replace("\u00a0", " ")
            try:
                split = nameText.split(". ")
                if len(split) > 1:
                    code = split[0]
                    title = split[1]
                else: # some courses (like 7 or 8) neglect the space
                    split = nameText.split(".")
                    code = split[0]
                    title = split[1]
                title = title[:title.find(" (")] # remove unit numbers
            except IndexError:
                logging.error(f"Couldn't split course title correctly, ignoring {nameText}")
                continue
            desc = name.findNextSibling().text.strip()
            if desc.find("Prerequisites:") != -1:
                desc = desc[:desc.find("Prerequisites:")].strip()

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


def get_config(): return {
  "name": "UC San Diego",
  "type": UCSDScraper,
}