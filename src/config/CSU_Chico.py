from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
    "name": "CSU Chico",
    "type": CourseLeafScraper,
    "subjectCodesUrl": "https://catalog.csuchico.edu/courses/",
    "selectors": {
        "code": ".detail-code",
        "title": ".detail-title",
        "description": ".detail-description",
    }
}