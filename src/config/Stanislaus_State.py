from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def get_config(): return {
    "name": "Stanislaus State",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.csustan.edu/content.php?catoid=32&navoid=5713",
    "selectors": {
        "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            0
        ],
        "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            1
        ],
    }
}