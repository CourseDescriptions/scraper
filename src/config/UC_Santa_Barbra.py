from scraper.common import fetch_soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        # going to have to use selenium from this part :(

        driver = webdriver.Firefox()
        driver.get(f"{BASE_LINK}/departments/{dept_name}/courses")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "coursesTabContent"))
        )
        links = element.find_elements(By.TAG_NAME, "a")
        hrefs = [link.get_attribute("href") for link in links]
        print("HREFS:", hrefs)
        driver.close()

        return hrefs


    def get_course(self, url: str) -> list[dict]:
        soup = fetch_soup(url)

        print(url)

        # return {
        #     "code": code,
        #     "title": title,
        #     "description": desc,
        #     "url": url
        # }

    def get(self, useCache: bool, limit: int | None = None) -> list[dict]:
        departments = self.get_department_names()

        print("DEPTS:", departments)

        courseUrls = []
        for dept in departments:
            courseUrls.extend(self.get_dept_course_urls(dept))

        data = []
        for url in courseUrls:
            data.append(self.get_course(url))

        return data

def get_config(): return {
  "name": "UC_Santa_Cruz",
  "type": UcsbScraper,
}