from urllib import parse
from scraper.common import fetch_json, fetch_soup, normalize_text

API_BASE = "https://api.ucla.edu/sis/publicapis/course"

class UclaScraper:
    """Course Descriptions Scraper for UCLA."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def fetch_and_parse_subjectarea_json(self, subj_area_cd: str, useCache: bool = True) -> list[dict]:
        subj_area_cd = parse.quote(subj_area_cd)
        course_data_json_url = f"{API_BASE}/getcoursedetail?subjectarea={subj_area_cd}"
        course_data_json = fetch_json(course_data_json_url, useCache)

        # Perform some basic munging to make the data returned from the UCLA API line
        #  up with data scraped from other sites.
        return [
            {
                "code": course["subj_area_cd"] + course["course_title"].split(".")[0],
                "title": course["course_title"].split(". ")[1],
                "description": course["crs_desc"],
                "url": course_data_json_url,
            }
            for course in course_data_json
        ]

    def get(self, useCache: bool = True, limit: int | None = None) -> list[dict]:
        """Get course descriptions for all subject codes."""

        # get from api
        subject_codes_json = fetch_json(f"{API_BASE}/getallcourses", useCache)
        data = [
            course
            for _ in subject_codes_json
            for course in self.fetch_and_parse_subjectarea_json(_["subj_area_cd"], useCache)
            if "LAW" not in course["code"]
        ]

        # get law courses that are only hosted on the law site specifically
        ucla_law_url = "https://curriculum.law.ucla.edu/Guide/AllCourses"
        soup = fetch_soup(ucla_law_url, useCache)

        course_page_links = []
        for course_abstract in soup.select(".course-abstract"):
            for link in course_abstract.select("a"):
                if "/Guide/Course" in link["href"] and "LAW" in link.text:
                    course_page_links.append(f"https://curriculum.law.ucla.edu{link["href"]}")

        law_data = []
        for link in course_page_links:
            soup = fetch_soup(link, useCache)
            head = normalize_text(soup.select_one(".document-header").text)
            desc = normalize_text(soup.select_one(".description.standard-body").text)
            law_data.append({
                "code": head.split(" - ")[0].upper(), # be consistent with other courses
                "title": head.split(" - ")[1],
                "description": desc,
                "url": link,
            })

        data.extend(law_data)

        return data

    def get_author(self):
        return "Simon Wiles"

def get_config(): return {
    "name": "UCLA",
    "type": UclaScraper,
    "author": "Rohan Parekh"
}