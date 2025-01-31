def get_config(): return {
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
    }