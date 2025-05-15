from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
  "name": "Cal Poly Humboldt",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.cpp.edu/content.php?catoid=68&navoid=5731",
  "selectors": {
      "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
          0
      ],
      "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
          1
      ],
  },
  "author": "Rohan Parekh"
}