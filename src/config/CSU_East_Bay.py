{
  "CSU_East_Bay": {
        "name": "CSU East Bay",
        "type": "moderncampus",
        "startUrl": "https://catalog.csueastbay.edu/content.php?catoid=35&navoid=30996",
        "selectors": {
            "code": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
                0
            ],
            "title": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
                1
            ],
        },
    },
}