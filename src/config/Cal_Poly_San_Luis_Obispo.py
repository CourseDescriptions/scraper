from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
    "name": "Cal Poly San Luis Obispo",
    "type": CourseLeafScraper,
    "subjectCodesUrl": "https://catalog.calpoly.edu/coursesaz/",
    "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      "description": ".courseblockextra:not(.noindent)",
  }
}