from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "San Jose State",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.sjsu.edu/content.php?catoid=15&navoid=5382",
    "selectors": {
        "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            0
        ],
        "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            1
        ],
    }
}