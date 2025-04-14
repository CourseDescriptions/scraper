from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "CSU_Fullerton",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.fullerton.edu/content.php?catoid=91&navoid=13418",
    "selectors": {
        "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            0
        ],
        "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            1
        ],
    }
}