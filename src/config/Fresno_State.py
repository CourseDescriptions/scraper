from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
  "name": "Fresno State",
  "type": ModernCampusScraper,
  "startUrl": "https://catalog.fresnostate.edu/content.php?catoid=5&navoid=193",
  "selectors": {
    "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
        0
    ],
    "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
        1
    ],
  }
}