from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
    "name": "Chico State",
    "type": CourseLeafScraper,
    "subjectCodesUrl": "https://catalog.csuchico.edu/courses/",
    "selectors": {
        "code": ".detail-code",
        "title": ".detail-title",
        "description": ".detail-description",
    }
}