from scraper.moderncampus import ModernCampusScraper
import logging
logger = logging.getLogger("__name__")
from scraper.common import normalize_text

def get_desc(el):
    # Find the course title
    title = el.select_one("#course_preview_title")

    texts = []
    for child in title.parent.contents:
        text = child.text.strip()
        texts.append(text)

    # get rid of everything before units
    if "Unit(s):" in texts:
        texts = texts[texts.index("Unit(s):")+2 : ] # +2 to get rid of unit count as well

    # get first instance of sublist ['', ''] which seems consistent marker for end of description?
    target = ['', '']

    res = -1
    for idx in range(len(texts) - len(target) + 1):
        if texts[idx: idx + len(target)] == target:
            res = idx
            break
    if res == -1:
        logger.error("Could not find target sublist when looking for course description")
        return ""
    
    # slice off after target
    texts = texts[ : idx]

    # get rid of empty lines
    texts = [line for line in texts if line != ""]

    return " ".join([text for text in texts if text != ""])

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