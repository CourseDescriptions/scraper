def get_config(): return {
    "name": "San Diego State",
    "type": "moderncampus",
    "startUrl": "https://catalog.sdsu.edu/content.php?catoid=9&navoid=776",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split("\xa0-\xa0")[
            1
        ],
    }
}