from scraper.moderncampus import ModernCampusScraper

def get_config(): return {
    "name": "CSU San Marcos",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.csusm.edu/content.php?catoid=10&navoid=1811",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ]
    }
}