def get_config(): return {
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