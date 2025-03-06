from scraper.moderncampus import ModernCampusScraper

def get_config(): return {
    "name": "San Jose State",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.sjsu.edu/content.php?catoid=15&navoid=5382",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
    }
}