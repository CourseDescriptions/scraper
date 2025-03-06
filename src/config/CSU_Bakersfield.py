from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
  "name": "CSU Bakersfield",
  "type": CourseLeafScraper,
  "subjectCodesUrl": "https://catalog.csub.edu/course-descriptions/",
  "selectors": {
      "code": ".detail-code",
      "title": ".detail-title",
      # Permit missing description (.courseblockextra) element
      "description": lambda el: getattr(
          el.select_one(".courseblockextra"), "text", ""
      ),
  }
}