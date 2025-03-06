from scraper.moderncampus import ModernCampusScraper

def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.cpp.edu/content.php?catoid=68&navoid=5731",
  "selectors": {
      "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
          0
      ],
      "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
          1
      ],
  }
}