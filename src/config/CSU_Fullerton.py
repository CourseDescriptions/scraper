from scraper.moderncampus import ModernCampusScraper


def get_config(): return {
    "name": "CSU_Fullerton",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.fullerton.edu/content.php?catoid=91&navoid=13418",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
    }
}