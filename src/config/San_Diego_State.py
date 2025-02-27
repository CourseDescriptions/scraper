def get_desc(el):
    # Find the course title
    title = el.select_one("#course_preview_title")

    # Find the next non-empty sibling (if it's an empty <strong> tag, skip it)
    siblings = title.find_all_next("strong")

    # Find the first sibling with text after an empty <strong> tag
    for strong in siblings:
        if not strong.get_text(strip=True):
            print(strong.text)
            print(strong.find_next_sibling())

    return el.select_one("#course_preview_title").text.split("\xa0-\xa0")[1]

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
        "description": lambda el: get_desc(el)
        
    }
}