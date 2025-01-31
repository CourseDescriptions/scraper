from pathlib import Path

# relative to this config file
CACHE_DIR = Path(__file__).parent.parent.parent / "cache"

SITES = {
    "Fresno_State": {
        "name": "Fresno State",
        "type": "moderncampus",
        "startUrl": "https://catalog.fresnostate.edu/content.php?catoid=5&navoid=193",
        "selectors": {
            "code": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
                0
            ],
            "title": lambda el: el.select_one("#course_preview_title").text.split(" - ")[
                1
            ],
        },
    },
    "UC_Berkeley": {
        "name": "UC Berkeley",
        "type": "courseleaf",
        "subjectCodesUrl": "https://guide.berkeley.edu/courses/",
        "selectors": {
            "code": ".courseblocktitle .code",
            "title": ".courseblocktitle .title",
            # Text content from the .descshow element minus the part before the first
            #  <br/> element plus the text from the .deschide element if it exists
            "description": lambda el: (
                descshow := el.select_one(".descshow"),
                descshow.contents[0].extract(),
                descshow.text,
            )[-1]
            + getattr(el.select_one(".deschide"), "text", ""),
        },
    },
    "UC_Davis": {
        "name": "UC Davis",
        "type": "courseleaf",
        "subjectCodesUrl": "https://catalog.ucdavis.edu/courses-subject-code/",
        "selectors": {
            "code": ".detail-code b",
            "title": lambda el: el.select_one(".detail-title b").text.lstrip("— "),
            # Text content from the .courseblockextra element minus the part before
            #  the first <br/> element
            "description": lambda el: (
                courseblockextra := el.select_one(".courseblockextra"),
                courseblockextra.contents[0].extract(),
                courseblockextra.text,
            )[-1],
        },
    },
    "UC_Irvine": {
        "name": "UC Irvine",
        "type": "courseleaf",
        "subjectCodesUrl": "https://catalogue.uci.edu/allcourses/",
        "selectors": {
            "code": lambda el: el.select_one(".courseblocktitle strong").text.split(
                ".  "
            )[0],
            "title": lambda el: el.select_one(".courseblocktitle strong").text.split(
                ".  "
            )[1],
            "description": ".courseblockdesc p:first-child",
        },
    },
    "UCLA": {
        "name": "UCLA",
        "type": "ucla",
    },
    "UC_San_Francisco": {
        "name": "UC San Francisco",
        "type": "courseleaf",
        "subjectCodesUrl": "https://catalog.ucsf.edu/course-catalog/",
        "selectors": {
            "code": ".detail-code",
            "title": ".detail-title",
            "description": ".courseblockextra:not(.noindent)",
        },
    },
}
