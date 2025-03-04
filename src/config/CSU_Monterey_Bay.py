def get_config(): return {
    "name": "CSU Monterey Bay",
    "type": "moderncampus",
    "startUrl": "https://catalog.csumb.edu/content.php?catoid=10&navoid=549",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
    }
}