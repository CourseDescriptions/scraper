from scraper.common import fetch_soup
import logging
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_LINK = "https://catalog.ucsb.edu"

class UcsbScraper:
    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def get_department_names(self) -> list[str]:
        soup = fetch_soup(BASE_LINK + "/departments")
        links = soup.find_all("a")
        return [link["href"].split("/")[2] for link in links
                if "overview" in link["href"]]

    def get_dept_course_urls(self, dept_name: str) -> list[str]:
        driver = webdriver.Firefox()
        for i in range(3):
            print("Getting, try:", i)
            driver.get(f"{BASE_LINK}/departments/{dept_name}/courses")
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "coursesTabContent"))
                )
                break
            except TimeoutException:
                if driver.find_elements(By.ID, "captcha-container"):
                    sleep(30)
                    continue
                logging.error(f"Waited too long while trying to get course urls from\
                              {BASE_LINK}/departments/{dept_name}/courses, skipping!")
                driver.close()
                return []
        
        links = element.find_elements(By.TAG_NAME, "a")
        hrefs = [link.get_attribute("href") for link in links]
        # print("HREFS:", hrefs)
        driver.close()

        return hrefs


    def get_course(self, url: str) -> list[dict]:
        soup = fetch_soup(url)
        main = soup.select_one("#main-content")

        codeTitle = main.select_one(".heading-5.mb-2").text.strip()

        code = codeTitle.split(" - ")[0]
        title = codeTitle.split(" - ")[1]

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

        # print("DEPTS:", departments)

        courseUrls = []
        for dept in departments:
            courseUrls.extend(self.get_dept_course_urls(dept))
            if limit and len(courseUrls) > limit:
                courseUrls = courseUrls[:limit]
                break

        data = []
        for url in courseUrls:
            data.append(self.get_course(url))

        return data

def get_config(): return {
  "name": "UC_Santa_Cruz",
  "type": UcsbScraper,
}