def get_config(): return {
        "name": "CSU Dominguez Hills",
        "type": "courseleaf",
        "subjectCodesUrl": "https://catalog.csudh.edu/courses/",
        "selectors": {
            "code": lambda el: el.select_one(".detail-code").text.rstrip("."),
            "title": lambda el: el.select_one(".detail-title").text.rstrip("."),
            # The last .courseblockextra element is always "Offered ...", but sometimes
            #  it's the only one; take a description only if there's more than one
            "description": lambda el: (
                courseblockextra := el.select(".courseblockextra"),
                "" if not len(courseblockextra) > 1 else courseblockextra[0].text,
            )[-1],
        },
    },