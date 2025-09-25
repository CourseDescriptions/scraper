from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
  "name": "University of Illinois Urbana-Champaign",
  "type": CourseLeafScraper,
  "subjectCodesUrl": "http://catalog.illinois.edu/courses-of-instruction/",
  "selectors": {
    "code": lambda el : el.select_one(".courseblocktitle").text.split(" \u2002 ")[0],
    "title": lambda el : el.select_one(".courseblocktitle").text.split(" \u2002 ")[1],
    "description": ".courseblockdesc",
  },
  "author": "Rohan Parekh"
}