from scraper.courseleaf import CourseLeafScraper

def get_config(): return {
    "name": "Cal Poly San Luis Obispo",
    "type": CourseLeafScraper,
    "subjectCodesUrl": "https://catalog.calpoly.edu/coursesaz/",
    "subjectCodeSelector": ".sitemaplink",
    "selectors": {
      "code": lambda el: el.select_one(".courseblocktitle strong").text.split(". ")[0],
      "title": lambda el: el.select_one(".courseblocktitle strong").text.split(". ")[1],
      "description": ".courseblockdesc",
  },
  "author": "Rohan Parekh"
}