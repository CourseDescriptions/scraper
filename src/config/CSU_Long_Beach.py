def get_config(): return {
    "name": "CSU Long Beach",
    "type": "moderncampus",
    "startUrl": "http://catalog.csulb.edu/content.php?catoid=10&navoid=1156",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title")\
        .text.split("\xa0-\xa0")[0],
        "title": lambda el: el.select_one("#course_preview_title")\
        .text.split("\xa0-\xa0")[1],
    }
}