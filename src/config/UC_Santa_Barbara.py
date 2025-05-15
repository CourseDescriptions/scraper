from scraper.common import fetch_soup_retries
from scraper.common import get_cache_path_for_url
import logging
from time import sleep
from requests.exceptions import HTTPError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup, Tag

import gzip

BASE_LINK = "https://catalog.ucsb.edu"

class UcsbScraper:
    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def get_department_names(self) -> list[str]:
        soup = fetch_soup_retries(BASE_LINK + "/departments")
        links = soup.find_all("a")
        return [link["href"].split("/")[2] for link in links
                if "overview" in link["href"]]

    def get_dept_course_page_soup(self, dept_name: str, useCache: bool = True) -> Tag | None:
        url = f"{BASE_LINK}/departments/{dept_name}/courses"
        cache_path = get_cache_path_for_url(url, ext="html")
        if useCache and cache_path.exists():
            logging.info(f"Getting cached {url}")
            with gzip.open(cache_path, "rt", encoding="utf-8") as _fh:
                return BeautifulSoup(_fh.read(), "lxml")

        driver = webdriver.Firefox()
        for _ in range(3):
            driver.get(url)
            try:
                element = WebDriverWait(driver, 10).until(
                    expected_conditions.presence_of_element_located(
                        (By.ID, "coursesTabContent")
                    )
                )
                break
            except TimeoutException:
                if driver.find_elements(By.ID, "captcha-container"):
                    sleep(30)
                    continue
                logging.error(f"Waited too long while trying to get course urls from\
                              {BASE_LINK}/departments/{dept_name}/courses, skipping!")
                # compress text and write to cache
                with gzip.open(cache_path, "wt", encoding="utf-8") as _fh:
                    _fh.write(driver.page_source)
                driver.close()
                return None
            
        # compress text and write to cache
        with gzip.open(cache_path, "wt", encoding="utf-8") as _fh:
            _fh.write(driver.page_source)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.close()
        return soup


    def get_dept_course_urls(self, dept_name: str, useCache: bool) -> list[str]:
        soup = self.get_dept_course_page_soup(dept_name, useCache)
        if soup == None:
            return []
        links = soup.find_all("a")
        hrefs = [BASE_LINK + link["href"] for link in links if "/courses/" in link["href"]]
        # print("HREFS:", hrefs)
        return hrefs

    def get_course(self, url: str) -> list[dict] | None:
        soup = fetch_soup_retries(url, retryWait=120)
        if soup == None:
            logging.error(f"Failed to get course {url}, skipping")
            return None
        main = soup.select_one("#main-content")

        codeTitle = main.select_one(".heading-5.mb-2").text.strip()

        codeTitleList = codeTitle.split(" - ")
        code = codeTitleList[0]
        if len(codeTitleList) >= 2:
            title = codeTitleList[1]
        else:
            title = ""
            logging.error(f"Could not find title in elem {codeTitle}")

        labels = main.select(".field-label")
        descLabels = [label for label in labels
            if "Course Description" in label.text]
        
        if len(descLabels) == 0:
            logging.error("Could not find description for course", url)
            desc = ""
        else:
            desc = descLabels[0].find_next_sibling().text.strip()

        return {
            "code": code,
            "title": title,
            "description": desc,
            "url": url
        }

    def get(self, useCache: bool, limit: int | None = None) -> list[dict]:
        departments = self.get_department_names()

        courseUrls = []
        for dept in departments:
            courseUrls.extend(self.get_dept_course_urls(dept, useCache))
            if limit and len(courseUrls) > limit:
                courseUrls = courseUrls[:limit]
                break

        print("Course urls:", courseUrls)
        data = []
        for url in courseUrls:
            course = self.get_course(url)
            if course == None: continue
            data.append(course)

        return data
    
    def get_author(self):
        return "Rohan Parekh"


def get_config(): return {
    "name": "UC_Santa_Barbara",
    "type": UcsbScraper,
    "author": "Rohan Parekh"
}