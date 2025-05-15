from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "CSU East Bay",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.csueastbay.edu/content.php?catoid=35&navoid=30996",
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