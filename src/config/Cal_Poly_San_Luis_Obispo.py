def get_config(): return {
    "name": "Cal Poly San Luis Obispo",
    "type": "moderncampus",
    "startUrl": "https://catalog.calpoly.edu/coursesaz/",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
    }
}