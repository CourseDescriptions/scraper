from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "CSU Monterey Bay",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.csumb.edu/content.php?catoid=10&navoid=549",
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