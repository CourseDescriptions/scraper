from urllib import parse

from scraper.common import fetch_json

API_BASE = "https://api.ucla.edu/sis/publicapis/course"


class UclaScraper:
    """Course Descriptions Scraper for UCLA."""

    def __init__(self, site_config: dict) -> None:
        self.config = site_config

    def fetch_and_parse_subjectarea_json(self, subj_area_cd: str) -> list[dict]:
        subj_area_cd = parse.quote(subj_area_cd)
        course_data_json_url = f"{API_BASE}/getcoursedetail?subjectarea={subj_area_cd}"
        course_data_json = fetch_json(course_data_json_url)

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

        subject_codes_json = fetch_json(f"{API_BASE}/getallcourses")

        data = [
            course
            for _ in subject_codes_json
            for course in self.fetch_and_parse_subjectarea_json(_["subj_area_cd"])
        ]
        return data
