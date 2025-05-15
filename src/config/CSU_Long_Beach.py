from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "CSU Long Beach",
    "type": ModernCampusScraper,
    "startUrl": "http://catalog.csulb.edu/content.php?catoid=10&navoid=1156",
    "selectors": {
        "code": lambda el: normalize_text(el.select_one("#course_preview_title")\
        .text).split(" - ")[0],
        "title": lambda el: normalize_text(el.select_one("#course_preview_title")\
        .text).split(" - ")[1],
    },
    "author": "Rohan Parekh"
}