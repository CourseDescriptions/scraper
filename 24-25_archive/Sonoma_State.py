from scraper.moderncampus import ModernCampusScraper
import logging
logger = logging.getLogger("__name__")
from scraper.common import normalize_text

def get_desc(el):
    # Find the course title
    content = el.select_one(".block_content")
    hr_strongs = content.select("hr + strong")
    if not len(hr_strongs):
        start = content.select_one("#course_preview_title")
    if len(hr_strongs) == 1:
        start = content.select_one("hr + strong ~ hr")
    else:
        start = content.select_one("hr + strong ~ br")

    end = content.select_one("br + br")

    text = []
    for sibling in start.next_siblings:
        if sibling == end:
            break
        text.append(sibling.text.strip())

    return normalize_text("\n".join(text))


def get_config(): return {
    "name": "Sonoma State",
    "type": ModernCampusScraper,
    "startUrl": "https://catalog.sonoma.edu/content.php?catoid=11&navoid=1421",
    "selectors": {
        "code": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            0
        ],
        "title": lambda el: normalize_text(el.select_one("#course_preview_title").text).split(" - ")[
            1
        ],
        "description": get_desc
    },
    "author": "Rohan Parekh"
}