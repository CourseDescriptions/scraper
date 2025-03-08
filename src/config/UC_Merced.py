from scraper.moderncampus import ModernCampusScraper
from scraper.common import normalize_text

def extract(el):
    start = el.select_one("#course_preview_title ~ hr")

    content = []
    for sibling in start.next_siblings:
        if sibling.name == "hr" or sibling.name == "strong":
            break

        if sibling.name: continue
        if "Units:" in sibling.text: continue
        if "Unit Limit:" in sibling.text: continue

        content.append(sibling)

    return normalize_text(" ".join(content))

def get_config(): return {
    "name": "UC Merced",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.ucmerced.edu/content.php?catoid=23&navoid=2517",
    "selectors": {
        "code": lambda el: el.select_one("#course_preview_title").text.split(": ")[
            0
        ],
        "title": lambda el: el.select_one("#course_preview_title").text.split(": ")[
            1
        ],
        "description": lambda el: extract(el)
    }
}