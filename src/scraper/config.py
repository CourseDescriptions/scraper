from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent.parent / "cache"

SITES = {
    "UC_Berkeley": {
        "name": "UC Berkeley",
        "type": "squares",
        "urlBase": "https://guide.berkeley.edu",
        "subjectCodesUrl": "https://guide.berkeley.edu/courses/",
        "selectors": {
            "code": ".courseblocktitle .code",
            "title": ".courseblocktitle .title",
            "description": lambda el: el.select_one(".descshow br").nextSibling,
        },
    },
    "UC_Davis": {
        "name": "UC Davis",
        "type": "squares",
        "urlBase": "https://catalog.ucdavis.edu",
        "subjectCodesUrl": "https://catalog.ucdavis.edu/courses-subject-code/",
        "selectors": {
            "code": ".detail-code b",
            "title": lambda el: el.select_one(".detail-title b").text.lstrip("— "),
            "description": lambda el: el.select_one(".courseblockextra em").nextSibling,
        },
    },
}
