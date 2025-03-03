def get_config(): return {
    "name": "Stanislaus State",
    "type": "moderncampus",
    "startUrl": "https://catalog.csustan.edu/content.php?catoid=32&navoid=5713",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ]
    }
}