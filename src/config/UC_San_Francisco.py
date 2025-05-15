from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
  "name": "UC San Francisco",
  "type": CourseLeafScraper,
  "subjectCodesUrl": "https://catalog.ucsf.edu/course-catalog/",
  "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      "description": ".courseblockextra:not(.noindent)",
  },
  "author": "Rohan Parekh"
}